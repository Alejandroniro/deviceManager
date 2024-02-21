from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Auth, Device, DeviceExecution


# Create your views here.
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
