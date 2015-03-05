from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from usuarios.models import Empresa,Usuario

# Create your views here.
def Login(request):
	empresas = Empresa.objects.all()
	if request.method == 'POST':
		r_username = request.POST['username']
		r_password = request.POST['password']
		r_empresa = request.POST['empresa']
		usuario = authenticate(username=r_username, password=r_password)
		if usuario is not None:
			if usuario.is_active:
				try:
					usuario_empresa = Usuario.objects.get(usuario=r_username,empresa=r_empresa)
				except Usuario.DoesNotExist:
					return HttpResponseRedirect(reverse('usuarios:login'))
				login(request, usuario)
				return HttpResponseRedirect(reverse('almacen:bienvenida'))				
			else:
				return HttpResponseRedirect(reverse('usuarios:login'))				
		else:
			return HttpResponseRedirect(reverse('usuarios:login'))
	context = {'empresas':empresas}
	return render(request, 'usuarios/login.html', context)

