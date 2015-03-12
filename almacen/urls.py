from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from almacen.views import registrar_inventario_inicial,registrar_ingreso,busquedaSuministro, Inicio, CrearTipoIngreso, CrearAlmacen, CrearZona, CrearSuministro,CrearTipoUnidad,CrearTipoStock, CrearGrupoSuministros, upload_file, ListadoSuministros, DetalleSuministro, ModificarSuministro, KardexSuministro,ReporteKardexSuministro

urlpatterns = patterns('',
	url(r'^$', Inicio.as_view(), name="inicio"),
	url(r'^registrar_inventario_inicial/$',registrar_inventario_inicial, name="registrar_inventario_inicial"),
	url(r'^registrar_ingreso/$',registrar_ingreso, name="registrar_ingreso"),
	url(r'^busquedaSuministro/$',busquedaSuministro, name="busquedaSuministro"),
	url(r'^crear_tipo_ingreso/$', CrearTipoIngreso.as_view(), name="crear_tipo_ingreso"),
	url(r'^crear_almacen/$', CrearAlmacen.as_view(), name="crear_almacen"),
	url(r'^crear_zona/$', CrearZona.as_view(), name="crear_zona"),
	url(r'^crear_suministro/$', CrearSuministro.as_view(), name="crear_suministro"),
	url(r'^crear_tipo_unidad/$', CrearTipoUnidad.as_view(), name="crear_tipo_unidad"),
	url(r'^crear_tipo_stock/$', CrearTipoStock.as_view(), name="crear_tipo_stock"),
	url(r'^crear_grupo_suministros/$', CrearGrupoSuministros.as_view(), name="crear_grupo_suministros"),
	url(r'^upload_file/', upload_file, name="upload_file"),
	url(r'^reporte_suministros/$', ListadoSuministros.as_view(), name="reporte_suministros"),
	url(r'^suministros/(?P<pk>\d+)/$',DetalleSuministro.as_view(), name="detalle_suministro"),
	url(r'^modificar/(?P<pk>\d+)/$',ModificarSuministro.as_view(), name="modificar_suministro"),
	url(r'^kardex_suministro/$', KardexSuministro.as_view(), name="kardex_suministro"),
	url(r'^reporte_kardex_suministro/$', ReporteKardexSuministro.as_view(), name="reporte_kardex_suministro"),
)