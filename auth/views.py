from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Auth, Device, DeviceExecution



class AuthListView(ListView):
    model = Auth
    template_name = "Auth_list.html"


class AuthCreateView(CreateView):
    model = Auth
    template_name = "Auth_form.html"
    fields = ["email", "password"]


class AuthUpdateView(UpdateView):
    model = Auth
    template_name = "Auth_form.html"
    fields = ["email", "password"]


class AuthDeleteView(DeleteView):
    model = Auth
    template_name = "Auth_confirm_delete.html"
    success_url = reverse_lazy("Auth_list")
