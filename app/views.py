from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from django.shortcuts import get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DeviceCreationForm
from django.contrib.auth.models import User
from .models import Device, Device_execution
from .utils import ping_device
from django.utils import timezone
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del parámetro 1.'),
            'password1': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del parámetro 1.'),
            'password2': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del parámetro 1.')
        }
    )
)
@api_view(['POST'])
@csrf_exempt
def signup(request):
    """
    View para manejar el registro de usuarios.

    Método:
    - POST: Se espera un JSON con datos de usuario para el registro.

    Respuestas:
    - Success: Usuario registrado correctamente.
    - Error: Fallo en la validación o el email ya existe.
    """
    if request.method == "POST":
        try:

            form = CustomUserCreationForm(request.data)

            if form.is_valid():
                user = form.save()
                login(request, user)

                csrf_token = get_token(request)

                response_data = {"csrf_token": csrf_token}
                return JsonResponse(response_data)

            else:
                return JsonResponse({"error": form.errors})

        except IntegrityError:
            return JsonResponse({"error": "Email already exists"})

    return JsonResponse({"error": "Invalid request method"})

@api_view(['POST'])
@csrf_exempt
def signin(request):
    """
    View para manejar la autenticación de usuarios.

    Método:
    - POST: Se espera un JSON con credenciales de usuario para el inicio de sesión.

    Respuestas:
    - Success: Inicio de sesión exitoso con el token CSRF.
    - Error: Fallo en la validación o credenciales incorrectas.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            form = CustomAuthenticationForm(data=data)

            if form.is_valid():
                user = authenticate(
                    request,
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"],
                )

                if user is not None:
                    login(request, user)

                    csrf_token = get_token(request)

                    response_data = {
                        "success": "Login successful",
                        "csrf_token": csrf_token,
                    }
                    return JsonResponse(response_data)
                else:
                    return JsonResponse({"error": "Authentication failed"})

            else:
                return JsonResponse({"error": "Invalid credentials"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"})

    return JsonResponse({"error": "Invalid request method"})

@api_view(['GET'])
def device_list(request):
    """
    View para obtener la lista de dispositivos.

    Método:
    - GET: Devuelve una lista de dispositivos en formato JSON.

    Respuestas:
    - Success: Lista de dispositivos.
    - Error: Método de solicitud no válido.
    """
    if request.method == "GET":
        devices = Device.objects.all()
        data = [
            {"id": device.id, "name": device.name, "ip_address": device.ip_address}
            for device in devices
        ]
        return JsonResponse({"success": True, "data": data})
    else:
        return JsonResponse({"success": False, "errors": "Invalid request method"})

@api_view(['GET'])
def device_detail(request, device_id):
    """
    View para obtener detalles de un dispositivo específico.

    Método:
    - GET: Devuelve los detalles de un dispositivo en formato JSON.

    Respuestas:
    - Success: Detalles del dispositivo.
    - Error: Dispositivo no encontrado o método de solicitud no válido.
    """
    device = (
        Device.objects.filter(pk=device_id).values("id", "name", "ip_address").first()
    )

    if device:
        return JsonResponse({"success": True, "data": device})
    else:
        return JsonResponse({"success": False, "errors": "device not found"})

@api_view(['POST'])
@csrf_protect
def device_create(request):
    """
    View para crear un nuevo dispositivo.

    Método:
    - POST: Se espera un JSON con datos para crear un dispositivo.

    Respuestas:
    - Success: Dispositivo creado correctamente.
    - Error: Fallo en la validación o método de solicitud no válido.
    """
    if request.method == "POST":
        try:
            form = DeviceCreationForm(request.data)
            if form.is_valid():
                device = form.save()
                return JsonResponse(
                    {"success": True, "message": "device created successfully"}
                )
            else:
                return JsonResponse({"success": False, "errors": form.errors})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "errors": "Invalid JSON data"})
    else:
        return JsonResponse({"success": False, "errors": "Invalid request method"})

@api_view(['PUT'])
@csrf_protect
def device_update(request, device_id):
    """
    View para actualizar un dispositivo existente.

    Método:
    - PUT: Se espera un JSON con datos para actualizar un dispositivo existente.

    Respuestas:
    - Success: Dispositivo actualizado correctamente.
    - Error: Fallo en la validación, dispositivo no encontrado o método de solicitud no válido.
    """
    try:
        device = get_object_or_404(Device, pk=device_id)

        if request.method == "PUT":
            form = DeviceCreationForm(request.data, instance=device)

            if form.is_valid():
                form.save()
                return JsonResponse(
                    {"success": True, "message": "Device updated successfully"}
                )
            else:
                return JsonResponse({"success": False, "errors": form.errors})
    except device.DoesNotExist:
        return JsonResponse({"error": f"Device with ID {device_id} does not exist"})
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "errors": "Invalid JSON data"})
    except Exception as e:
        return JsonResponse({"error": str(e), "device_id": device_id})

    return JsonResponse({"success": False, "errors": "Invalid request method"})

@api_view(['DELETE'])
@csrf_protect
def device_delete(request, device_id):
    """
    View para eliminar un dispositivo.

    Método:
    - DELETE: Elimina un dispositivo existente.

    Respuestas:
    - Success: Dispositivo eliminado correctamente.
    - Error: Dispositivo no encontrado, ejecución de prueba de ping existente, o método de solicitud no válido.
    """
    device = get_object_or_404(Device, pk=device_id)

    if request.method == "DELETE":
        has_executions = Device_execution.objects.filter(device=device).exists()

        if has_executions:
            return JsonResponse({"success": False, "errors": "device has associated ping executions. Cannot delete."})

        device.delete()
        return JsonResponse({"success": True, "message": "device deleted successfully"})
    else:
        return JsonResponse({"success": False, "errors": "Invalid request method"})

@api_view(['GET'])
def device_execution_list(request):
    """
    View para obtener la lista de ejecuciones de dispositivos.

    Método:
    - GET: Devuelve una lista de ejecuciones de dispositivos en formato JSON.

    Respuestas:
    - Success: Lista de ejecuciones de dispositivos.
    - Error: Método de solicitud no válido.
    """
    if request.method == "GET":
        device_executions = Device_execution.objects.all()
        data = [
            {
                "id": execution.id,
                "execution_date": execution.execution_date,
                "device_id": execution.device.id,
                "was_successful": execution.was_successful,
            }
            for execution in device_executions
        ]
        return JsonResponse({"success": True, "data": data})
    else:
        return JsonResponse({"success": False, "errors": "Invalid request method"})

@api_view(['GET'])
def device_execution_detail(request, device_execution_id):
    """
    View para obtener detalles de una ejecución de dispositivo específica.

    Método:
    - GET: Devuelve los detalles de una ejecución de dispositivo en formato JSON.

    Respuestas:
    - Success: Detalles de la ejecución de dispositivo.
    - Error: Ejecución de dispositivo no encontrada o método de solicitud no válido.
    """
    device_execution = get_object_or_404(device_execution, pk=device_execution_id)
    data = {
        "id": device_execution.id,
        "execution_date": device_execution.execution_date,
        "device_id": device_execution.device.id,
        "was_successful": device_execution.was_successful,
    }
    return JsonResponse({"success": True, "data": data})

@api_view(['POST'])
@csrf_protect
def device_execution_ping(request, device_id):
    """
    View para realizar un ping a un dispositivo y registrar la ejecución.

    Método:
    - POST: Realiza un ping al dispositivo y registra la ejecución.

    Respuestas:
    - Success: Ping realizado correctamente.
    - Error: Dispositivo no encontrado, error en el ping o método de solicitud no válido.
    """
    try:
        device_instance = get_object_or_404(Device, id=device_id)
        ping_result = ping_device(device_instance.ip_address)

        device_execution_instance = Device_execution.objects.create(
            execution_date=timezone.now(), device=device_instance, was_successful=ping_result
        )

        if ping_result:
            device_execution_instance.total_success_count += 1
            device_execution_instance.historical_success_count += 1
        else:
            device_execution_instance.total_failure_count += 1
            device_execution_instance.historical_failure_count += 1

        device_execution_instance.save()

        return JsonResponse(
            {
                "success": f"Ping for device {device_id} was successful",
                "ping_result": ping_result,
            }
        )

    except Device.DoesNotExist:
        return JsonResponse({"error": f"Device with ID {device_id} does not exist"})
    except Exception as e:
        return JsonResponse({"error": str(e), "device_id": device_id})
