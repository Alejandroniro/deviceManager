from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from .forms import CustomUserCreationForm, CustomAuthenticationForm

@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))

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
            data = json.loads(request.body.decode('utf-8'))

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
                        "csrf_token": csrf_token
                    }
                    return JsonResponse(response_data)
                else:
                    return JsonResponse({"error": "Authentication failed"})

            else:
                return JsonResponse({"error": "Invalid credentials"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"})

    return JsonResponse({"error": "Invalid request method"})