from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from usuarios.views import Login

urlpatterns = patterns('',
	url(r'^$', Login, name="login"),
	url(r'^logout$', logout, {'template_name': 'usuarios/logout.html', }, name="logout"),
	)