from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from almacen.views import registrar_ingreso,busquedaSuministro, Bienvenida, CrearTipoIngreso, CrearAlmacen

urlpatterns = patterns('',
	url(r'^$', Bienvenida.as_view(), name="bienvenida"),
	url(r'^registrar_ingreso/$',registrar_ingreso, name="registrar_ingreso"),
	url(r'^busquedaSuministro/$',busquedaSuministro, name="busquedaSuministro"),
	url(r'^crear_tipo_ingreso/$', CrearTipoIngreso.as_view(), name="crear_tipo_ingreso"),
	url(r'^crear_almacen/$', CrearAlmacen.as_view(), name="crear_almacen"),
)