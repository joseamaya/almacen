from django.shortcuts import render
from almacen.models import Tipo, Almacen, Suministro, Movimiento, DetalleMovimiento, GrupoSuministros, Zona
from usuarios.models import Usuario
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.db import connection
import datetime,time
from django.views.generic import TemplateView, FormView
from almacen.forms import TipoIngresoForm, AlmacenForm, ZonaForm

# Create your views here.
def registrar_ingreso(request):
	tipo_mov='I'
	try: 
		tipo_movimiento = Tipo.objects.get(tabla="tipo_Movimiento",codigo=tipo_mov)
	except Tipo.DoesNotExist:
		tipo_movimiento = Tipo(tabla='tipo_Movimiento',descripcion_campo='tipo_Movimiento',codigo=tipo_mov,descripcion_valor='INGRESO')
		tipo_movimiento.save()
		return HttpResponseRedirect(reverse('almacen:registrar_ingreso'))
	tipos_ingreso = Tipo.objects.filter(tabla="tipo_Ingreso")
	if not tipos_ingreso:
		return HttpResponseRedirect(reverse('almacen:crear_tipo_ingreso'))	
	almacenes = Almacen.objects.all()
	if not almacenes:
		zonas = Zona.objects.all()
		if not zonas:
			return HttpResponseRedirect(reverse('almacen:crear_zona'))	 
		return HttpResponseRedirect(reverse('almacen:crear_almacen'))	
	tipos_documento = Tipo.objects.filter(tabla="tipo_Documento")
	suministros = Suministro.objects.all()
	if request.method == 'POST':
		tipo_ingreso=int(request.POST['tipos_ingreso'])
		tipo_documento=request.POST['tipos_documento']
		serie = request.POST['serie']
		numero = request.POST['numero']
		r_almacen = request.POST['almacenes']
		almacen = Almacen.objects.get(id=r_almacen)
		r_fecha = request.POST['fecha']
		anio = r_fecha[6:]
		mes = r_fecha[3:5]
		dia = int(r_fecha[0:2])
		fecha = datetime.date(int(anio),int(mes),dia)
		cdetalles = int(request.POST['cdetalles'])
		zona = almacen.zona
		empresa = almacen.empresa
		cod_movimiento=obtener_codigo_movimiento(tipo_movimiento, zona, anio, empresa)
		cod_orden = obtener_codigo_orden(tipo_movimiento.id, anio, mes, empresa)
		movimiento = Movimiento(cod_movimiento,tipo_movimiento.id_tabla_tipo,cod_orden,tipo_ingreso,
		tipo_documento,serie)
		movimiento.fecha = fecha
		movimiento.anio=anio
		movimiento.mes = mes
		movimiento.id_almacen = almacen
		movimiento.id_zona= zona
		movimiento.id_empresa= empresa
		movimiento.fecha_operacion=datetime.datetime.now()
		movimiento.numero = numero
		movimiento.mac = mac
		movimiento.id_subalmacen = '1'
		movimiento.usuario = 'miguel'
		movimiento.save()
		for i in range(cdetalles):
			id="tblDetalle_id_"+str(i+1)
			cant="tblDetalle_cantidad_"+str(i+1)
			prec="tblDetalle_precio_"+str(i+1)
			val="tblDetalle_valor_"+str(i+1)		
			id_suministro = request.POST[id]
			suministro = Suministros.objects.get(id_suministro=id_suministro)
			grupo_suministros = GrupoSuministros.objects.get(cod_grupo_sumi=suministro.cod_grupo_sumi)
			cantidad = request.POST[cant]
			precio= request.POST[prec]
			valor = request.POST[val]
			detalle = DetalleMovimiento(id=100006,nro_detallemovimiento=i+1,id_movimiento=cod_movimiento,
			id_suministro=id_suministro,cantidad=cantidad,precio=precio,fecha=fecha,id_zona=zona)	
			detalle.tipo_movimiento = tipo_movimiento.id_tabla_tipo
			detalle.valor = valor
			detalle.cta_cble_alm = grupo_suministros.ctaalm
			detalle.cta_cble = grupo_suministros.ctacomp
			detalle.save()
		#return HttpResponseRedirect(reverse('almacen:registrar_ingreso'))

	context = {'tipos_ingreso':tipos_ingreso,'almacenes':almacenes,'tipos_documento':tipos_documento,
	'suministros':suministros}
	return render(request, 'ingresar_movimiento.html', context)

def busquedaSuministro(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		suministros = Suministro.objects.filter(descripcion__icontains = q )[:20]	
		results = []
		for suministro in suministros:
			suministro_json = {}
			suministro_json['id'] = suministro.codigo
			suministro_json['label'] = suministro.descripcion
			suministro_json['value'] = suministro.descripcion
			unidad = Tipo.objects.get(id=suministro.tipo_unidad_medida.id,tabla='tipo_unidad_medida')			
			suministro_json['unidad'] = unidad.descripcion_valor
			suministro_json['precio'] = str(suministro.precio_mercado)			
			results.append(suministro_json)			
		data = json.dumps(results)		
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

def obtener_codigo_movimiento(tipo, zona, anio, empresa):
	movimientos = Movimiento.objects.filter(tipo_movimiento=tipo.id, almacen__zona=zona, fecha_operacion__year=anio,almacen__empresa=empresa).order_by('-id_movimiento')
	if not movimientos:
		aux = 1
	
	correlativo = str(aux).zfill(5)
	codigo = str(empresa.id)+str(tipo.codigo)+str(anio)+str(zona.id)+correlativo
	print(codigo)
	return codigo

'''def obtener_codigo_orden(tipo, anio, mes, empresa):
	cursor = connection.cursor()
	query = "SELECT fn_getcodigoorden(%i,'%s','%s','%s')" % (tipo, anio, mes, empresa)
	cursor.execute(query)
	row = cursor.fetchone()
	return row[0]'''

class Bienvenida(TemplateView):
	template_name = "bienvenida.html"

	def obtener_usuario(self):
		r_usuario=self.request.user
		return r_usuario

	def get_context_data(self, **kwargs): 
		return {'usuario': self.obtener_usuario()}

class CrearTipoIngreso(FormView):
    template_name = 'tipo_ingreso.html'
    form_class = TipoIngresoForm
    success_url = '/almacen/registrar_ingreso'

    def form_valid(self, form):
    	form.save()
    	return super(CrearTipoIngreso, self).form_valid(form)

class CrearAlmacen(FormView):
	template_name = 'almacen.html'
	form_class = AlmacenForm
	success_url = '/almacen/registrar_ingreso'

	def get_form(self, form_class):
		return form_class(self.request.user.empresa, **self.get_form_kwargs())

	def form_valid(self, form):
		form.save()
		return super(CrearAlmacen, self).form_valid(form)

class CrearZona(FormView):
    template_name = 'zona.html'
    form_class = ZonaForm
    success_url = '/almacen/registrar_ingreso'

    def form_valid(self, form):
    	form.save()
    	return super(CrearZona, self).form_valid(form)