from django.db import models


class Auth(models.Model):
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email


class Device(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class DeviceExecution(models.Model):
    execution_date = models.DateField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    was_successful = models.CharField(max_length=10)

    def __str__(self):
        return str(self.execution_date)
