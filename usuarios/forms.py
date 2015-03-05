from django import forms 
from django.contrib.auth.models import User
from usuarios.models import Empresa

class SignUpForm(forms.ModelForm):
	class Meta():
		model = User
		fields = ['username', 'password', 'email', 'first_name', 'last_name']
		widgets = {
			'password': forms.PasswordInput(),
		}
		labels = {
			'username': ('Usuario'),
			'email': ('Email'),
		}

class EmpresaForm(forms.ModelForm):
	class Meta():
		model = Empresa