from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=15)

    def __str__(self):
        return self.name
