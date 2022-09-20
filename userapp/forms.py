from django.contrib.auth.forms import UserCreationForm
from .models import HhUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = HhUser
        fields = ('username', 'password1', 'password2', 'email')
