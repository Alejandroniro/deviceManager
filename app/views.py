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


class DeviceListView(ListView):
    model = Device
    template_name = "device_list.html"


class DeviceCreateView(CreateView):
    model = Device
    template_name = "device_form.html"
    fields = ["name", "ip_address"]


class DeviceUpdateView(UpdateView):
    model = Device
    template_name = "device_form.html"
    fields = ["name", "ip_address"]


class DeviceDeleteView(DeleteView):
    model = Device
    template_name = "device_confirm_delete.html"
    success_url = reverse_lazy("device_list")


class DeviceExecutionListView(ListView):
    model = DeviceExecution
    template_name = "deviceexecution_list.html"


class DeviceExecutionCreateView(CreateView):
    model = DeviceExecution
    template_name = "deviceexecution_form.html"
    fields = ["execution_date", "device", "was_successful"]


class DeviceExecutionUpdateView(UpdateView):
    model = DeviceExecution
    template_name = "deviceexecution_form.html"
    fields = ["execution_date", "device", "was_successful"]


class DeviceExecutionDeleteView(DeleteView):
    model = DeviceExecution
    template_name = "deviceexecution_confirm_delete.html"
    success_url = reverse_lazy("deviceexecution_list")
