from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Device, DeviceExecution


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
