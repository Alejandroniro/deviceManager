from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
import subprocess
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DeviceCreationForm
from django.shortcuts import render, get_object_or_404
from .models import Device, DeviceManager
from .utils import ping_device
from django.utils import timezone



@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            form = CustomUserCreationForm(data)

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


@csrf_exempt
def signin(request):
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


# View para obtener la lista de dispositivos
def device_list(request):
    if request.method == "GET":
        devices = Device.objects.all()
        data = [
            {"id": device.id, "name": device.name, "ip_address": device.ip_address}
            for device in devices
        ]
        return JsonResponse({"success": True, "data": data})
    else:
        return JsonResponse({"success": False, "errors": "Invalid request method"})


# View para obtener detalles de un dispositivo
def device_detail(request, device_id):
    device = (
        Device.objects.filter(pk=device_id).values("id", "name", "ip_address").first()
    )

    if device:
        return JsonResponse({"success": True, "data": device})
    else:
        return JsonResponse({"success": False, "errors": "Device not found"})


# View para crear un nuevo dispositivo
def device_create(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            form = DeviceCreationForm(data)
            if form.is_valid():
                device = form.save()
                return JsonResponse(
                    {"success": True, "message": "Device created successfully"}
                )
            else:
                return JsonResponse({"success": False, "errors": form.errors})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "errors": "Invalid JSON data"})
    else:
        return JsonResponse({"success": False, "errors": "Invalid request method"})


# View para actualizar un dispositivo existente
def device_update(request, device_id):
    device = get_object_or_404(Device, pk=device_id)

    if request.method == "PUT":
        try:
            data = json.loads(request.body.decode("utf-8"))
            form = DeviceCreationForm(data, instance=device)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {"success": True, "message": "Device updated successfully"}
                )
            else:
                return JsonResponse({"success": False, "errors": form.errors})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "errors": "Invalid JSON data"})
    else:
        return JsonResponse({"success": False, "errors": "Invalid request method"})


# View para eliminar un dispositivo
def device_delete(request, device_id):
    device = get_object_or_404(Device, pk=device_id)

    if request.method == "DELETE":
        device.delete()
        return JsonResponse({"success": True, "message": "Device deleted successfully"})
    else:
        return JsonResponse({"success": False, "errors": "Invalid request method"})


def device_manager_list(request):
    if request.method == "GET":
        device_managers = DeviceManager.objects.all()
        data = [
            {
                "id": manager.id,
                "execution_date": manager.execution_date,
                "device_id": manager.device.id,
                "was_successful": manager.was_successful,
            }
            for manager in device_managers
        ]
        return JsonResponse({"success": True, "data": data})
    else:
        return JsonResponse({"success": False, "errors": "Invalid request method"})


def device_manager_detail(request, device_manager_id):
    device_manager = get_object_or_404(DeviceManager, pk=device_manager_id)
    data = {
        "id": device_manager.id,
        "execution_date": device_manager.execution_date,
        "device_id": device_manager.device.id,
        "was_successful": device_manager.was_successful,
    }
    return JsonResponse({"success": True, "data": data})


def device_manager_ping(request, device_id):
    try:
        device = get_object_or_404(Device, id=device_id)

        # Realizar el ping utilizando la dirección IP del dispositivo
        ping_result = ping_device(device.ip_address)

        # Crear un nuevo objeto DeviceManager y actualizar los campos estadísticos
        device_manager = DeviceManager.objects.create(
            execution_date=timezone.now().date(),
            device=device,
            was_successful=ping_result
        )

        # Actualizar estadísticas globales en DeviceManager
        if ping_result:
            device_manager.total_success_count = 1
            device_manager.historical_success_count += 1
        else:
            device_manager.total_failure_count = 1
            device_manager.historical_failure_count += 1

        device_manager.save()

        return JsonResponse({"success": f"Ping for Device {device_id} was successful", "ping_result": ping_result})

    except Exception as e:
        return JsonResponse({"error": str(e), "device_id": device_id})


def device_manager_delete(request, device_manager_id):
    device_manager = get_object_or_404(DeviceManager, pk=device_manager_id)

    if request.method == "DELETE":
        device_manager.delete()
        return JsonResponse(
            {"success": True, "message": "DeviceManager deleted successfully"}
        )
    else:
        return JsonResponse({"success": False, "errors": "Invalid request method"})
