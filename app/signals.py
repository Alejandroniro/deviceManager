from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Device

@receiver(post_migrate)
def seed_data(sender, **kwargs):
    if sender.name == 'app':
        print("La función seed_data se está ejecutando.")
        device_data = [
            {"name": "Google", "ip_address": "8.8.8.8"},
            {"name": "Localhost", "ip_address": "127.0.0.1"},
            {"name": "xbtech", "ip_address": "112.1.43.45"},
            {"name": "externo01", "ip_address": "190.17.45.10"},
        ]

        for data in device_data:
            Device.objects.create(name=data["name"], ip_address=data["ip_address"])