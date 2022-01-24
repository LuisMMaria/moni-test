# Imports from django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Import from drf
from rest_framework.authtoken.models import Token


# User model
class User(AbstractUser):
    # Fields
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField('Correo Electrónico', max_length=255,
                              unique=True)
    name = models.CharField('Nombres', max_length=255)
    last_name = models.CharField('Apellidos', max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']

    USERNAME_FIELD = 'username'
    # Minimum required fields
    REQUIRED_FIELDS = ['email', 'name', 'last_name', 'password']

    def natural_key(self):
        return (self.username)

    def __str__(self):
        return self.username


# Create a token when a user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
