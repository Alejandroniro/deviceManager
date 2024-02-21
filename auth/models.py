from django.db import models

class Auth(models.Model):
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email
