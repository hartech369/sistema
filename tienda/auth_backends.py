# auth_backends.py
from django.contrib.auth.backends import BaseBackend
from .models import Persona

class PersonaAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            persona = Persona.objects.get(email=email)
            if persona.check_password(password):
                return persona
        except Persona.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Persona.objects.get(pk=user_id)
        except Persona.DoesNotExist:
            return None