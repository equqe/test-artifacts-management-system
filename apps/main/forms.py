from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Tester

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = Tester
        fields = UserCreationForm.Meta.fields + ("email", )