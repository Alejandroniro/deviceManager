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
    operation_summary="Manejar el registro de usuarios.",
    operation_description="Realiza el registro de un nuevo usuario utilizando datos proporcionados en un JSON.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de correo electrónico del usuario.'),
            'password1': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña para el usuario.'),
            'password2': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmación de la contraseña.'),
        }
    ),
    responses={
        200: openapi.Response(description="Usuario registrado correctamente."),
        400: openapi.Response(description="Fallo en la validación o el email ya existe."),
        405: openapi.Response(description="Método de solicitud no válido."),
    }
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
                return JsonResponse({"error": form.errors}, status=400)

        except IntegrityError as e:
            # Agrega un bloque específico para ValidationError
            if 'unique constraint' in str(e):
                return JsonResponse({"error": "Email ya existe"}, status=400)
            else:
                return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método de solicitud no válido"}, status=405)


@swagger_auto_schema(
    methods=['post'],
    operation_summary="Manejar la autenticación de usuarios.",
    operation_description="Realiza el inicio de sesión de un usuario utilizando credenciales proporcionadas en un JSON.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de usuario o dirección de correo electrónico.'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario.'),
        }
    ),
    responses={
        200: openapi.Response(description="Inicio de sesión exitoso con el token CSRF."),
        401: openapi.Response(description="Fallo en la validación o credenciales incorrectas."),
        400: openapi.Response(description="Datos JSON no válidos o método de solicitud no válido."),
    }
)
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

            form = CustomAuthenticationForm(data=request.data)

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
                        "success": "Inicio de sesión exitoso",
                        "csrf_token": csrf_token,
                    }
                    return JsonResponse(response_data)
                else:
                    return JsonResponse({"error": "Fallo en la autenticación"}, status=401)

            else:
                return JsonResponse({"error": "Credenciales no válidas"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos JSON no válidos"}, status=400)

    return JsonResponse({"error": "Método de solicitud no válido"}, status=400)



@swagger_auto_schema(
    methods=['get'],
    operation_summary="Obtener la lista de dispositivos.",
    operation_description="Devuelve una lista de dispositivos en formato JSON.",
    responses={
        200: openapi.Response(description="Lista de dispositivos."),
        400: openapi.Response(description="Método de solicitud no válido."),
    }
)
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


@swagger_auto_schema(
    methods=['get'],
    operation_summary="Obtener detalles de un dispositivo específico.",
    operation_description="Devuelve los detalles de un dispositivo identificado por su ID en formato JSON.",
    responses={
        200: openapi.Response(description="Detalles del dispositivo."),
        404: openapi.Response(description="Dispositivo no encontrado."),
        400: openapi.Response(description="Método de solicitud no válido."),
    }
)
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
        return JsonResponse({"success": False, "errors": "device not found"}, status=404)


@swagger_auto_schema(
    methods=['post'],
    operation_summary="Crear un nuevo dispositivo.",
    operation_description="Crea un nuevo dispositivo mediante un JSON con datos de creación.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del nuevo dispositivo.'),
            'ip_address': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección IP del nuevo dispositivo.'),
        }
    ),
    responses={
        200: openapi.Response(description="Dispositivo creado correctamente."),
        400: openapi.Response(description="Fallo en la validación o método de solicitud no válido."),
    }
)
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


@swagger_auto_schema(
    methods=['put'],
    operation_summary="Actualizar un dispositivo existente.",
    operation_description="Actualiza un dispositivo existente mediante un JSON con datos actualizados.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo nombre del dispositivo.'),
            'ip_address': openapi.Schema(type=openapi.TYPE_STRING, description='Nueva dirección IP del dispositivo.'),
        }
    ),
    responses={
        200: openapi.Response(description="Dispositivo actualizado correctamente."),
        404: openapi.Response(description="Dispositivo no encontrado."),
        400: openapi.Response(description="Fallo en la validación, dispositivo no encontrado o método de solicitud no válido."),
    }
)
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
        return JsonResponse({"error": f"Device with ID {device_id} does not exist"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "errors": "Invalid JSON data"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e), "device_id": device_id}, status=404)

    return JsonResponse({"success": False, "errors": "Invalid request method"}, status=404)


@swagger_auto_schema(
    methods=['delete'],
    operation_summary="Eliminar un dispositivo.",
    operation_description="Elimina un dispositivo existente.",
    responses={
        200: openapi.Response(description="Dispositivo eliminado correctamente."),
        404: openapi.Response(description="Dispositivo no encontrado."),
        400: openapi.Response(description="Dispositivo tiene ejecuciones de prueba de ping asociadas o método de solicitud no válido."),
    }
)
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


@swagger_auto_schema(
    methods=['get'],
    operation_summary="Obtener la lista de ejecuciones de dispositivos.",
    operation_description="Devuelve una lista de ejecuciones de dispositivos en formato JSON.",
    responses={
        200: openapi.Response(description="Lista de ejecuciones de dispositivos."),
        400: openapi.Response(description="Método de solicitud no válido."),
    }
)
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


@swagger_auto_schema(
    methods=['get'],
    operation_summary="Obtener detalles de una ejecución de dispositivo específica.",
    operation_description="Devuelve los detalles de una ejecución de dispositivo identificada por su ID en formato JSON.",
    responses={
        200: openapi.Response(description="Detalles de la ejecución de dispositivo."),
        404: openapi.Response(description="Ejecución de dispositivo no encontrada."),
        400: openapi.Response(description="Método de solicitud no válido."),
    }
)
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
    device_execution_instance = get_object_or_404(Device_execution, pk=device_execution_id)
    data = {
        "id": device_execution_instance.id,
        "execution_date": device_execution_instance.execution_date,
        "device_id": device_execution_instance.device.id,
        "was_successful": device_execution_instance.was_successful,
    }
    return JsonResponse({"success": True, "data": data})


@swagger_auto_schema(
    methods=['post'],
    operation_summary="Realizar ping a un dispositivo y registrar la ejecución.",
    operation_description="Realiza un ping al dispositivo identificado por su ID y registra los resultados de la ejecución.",
    
    responses={
        200: openapi.Response(description="Ping realizado correctamente."),
        404: openapi.Response(description="Dispositivo no encontrado."),
        400: openapi.Response(description="Error en el ping o método de solicitud no válido."),
    }
)
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
        return JsonResponse({"error": f"Device with ID {device_id} does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e), "device_id": device_id}, status=400)