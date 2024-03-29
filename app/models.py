from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(protocol='IPv4')

    def __str__(self):
        return self.name


class Device_execution(models.Model):
    execution_date = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, db_index=True)
    was_successful = models.BooleanField()
    total_success_count = models.PositiveIntegerField(default=0)
    total_failure_count = models.PositiveIntegerField(default=0)
    historical_success_count = models.PositiveIntegerField(default=0)
    historical_failure_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.device.name} - {self.execution_date}"
