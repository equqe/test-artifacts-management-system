from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Tester, Projects

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = Tester
        fields = UserCreationForm.Meta.fields + ("email", )

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['project_name', 'description']

        widgets = {
            'project_name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }