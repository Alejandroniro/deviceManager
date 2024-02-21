from django.db import models
from device.models import Device


class DeviceExecution(models.Model):
    execution_date = models.DateField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    was_successful = models.CharField(max_length=10)

    def __str__(self):
        return str(self.execution_date)
