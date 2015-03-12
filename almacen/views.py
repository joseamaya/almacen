from django.shortcuts import render
from almacen.models import Tipo, Almacen, Suministro, Movimiento, DetalleMovimiento, GrupoSuministros, Zona, CuentaContable, Archivo, SuministroEmpresa, Kardex
from usuarios.models import Usuario
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.db import connection
import datetime,time
from django.views.generic import TemplateView, FormView, View, ListView, DetailView, UpdateView
from almacen.forms import TipoIngresoForm, AlmacenForm, ZonaForm, SuministroForm, TipoUnidadForm, TipoStockForm, GrupoSuministrosForm, UploadForm
import csv
from django.db.models import Max, Sum
from decimal import Decimal

def registrar_inventario_inicial(request):
	almacenes = Almacen.objects.all()
	t_mov='I'
	try: 
		tipo_movimiento = Tipo.objects.get(tabla="tipo_Movimiento",codigo=t_mov)
	except Tipo.DoesNotExist:
		tipo_movimiento = Tipo(tabla='tipo_Movimiento',descripcion_campo='tipo_Movimiento',codigo=t_mov,descripcion_valor='INGRESO')
		tipo_movimiento.save()
	t_ing = 'I00'
	try: 
		tipo_ingreso = Tipo.objects.get(tabla='tipo_Ingreso',codigo=t_ing)
	except Tipo.DoesNotExist:
		tipo_ingreso = Tipo(tabla='tipo_Ingreso',descripcion_campo='tipo_Ingreso',codigo=t_ing,descripcion_valor='INGRESO POR INVENTARIO INICIAL')
		tipo_ingreso.save()

	if request.method == 'POST':
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
		movimiento = Movimiento(cod_movimiento,tipo_movimiento.id,tipo_ingreso.id)
		movimiento.anio=anio
		movimiento.mes = mes
		movimiento.almacen = almacen
		movimiento.fecha_operacion=fecha
		movimiento.usuario = request.user.usuario
		movimiento.observacion = 'Inventario inicial'
		movimiento.save()
		for i in range(cdetalles):
			id="tblDetalle_id_"+str(i+1)
			cant="tblDetalle_cantidad_"+str(i+1)
			prec="tblDetalle_precio_"+str(i+1)
			val="tblDetalle_valor_"+str(i+1)		
			id_suministro = request.POST[id]
			suministro = Suministro.objects.get(codigo=id_suministro)
			grupo_suministros = GrupoSuministros.objects.get(codigo=suministro.grupo_suministros.codigo)
			cantidad = Decimal(request.POST[cant])			
			precio= Decimal(request.POST[prec])
			valor = Decimal(request.POST[val])
			detalle = DetalleMovimiento(nro_detalle=i+1,movimiento=movimiento,suministro=suministro)
			detalle.cantidad=cantidad
			detalle.precio=precio
			detalle.valor = valor
			detalle.save()
			return HttpResponseRedirect(reverse('almacen:inicio'))
	context = {'almacenes':almacenes}
	return render(request, 'inventario_inicial.html', context)

def registrar_ingreso(request):	
	tipos_ingreso = Tipo.objects.exclude(codigo='I00').filter(tabla="tipo_Ingreso")
	t_mov='I'
	try: 
		tipo_movimiento = Tipo.objects.get(tabla="tipo_Movimiento",codigo=t_mov)
	except Tipo.DoesNotExist:
		tipo_movimiento = Tipo(tabla='tipo_Movimiento',descripcion_campo='tipo_Movimiento',codigo=t_mov,descripcion_valor='INGRESO')
		tipo_movimiento.save()
	if not tipos_ingreso:
		return HttpResponseRedirect(reverse('almacen:crear_tipo_ingreso'))	
	almacenes = Almacen.objects.filter()		
	tipos_documento = Tipo.objects.filter(tabla="tipo_Documento")
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
		movimiento = Movimiento(cod_movimiento,tipo_movimiento.id,tipo_ingreso,tipo_documento,serie)
		movimiento.anio=anio
		movimiento.mes = mes
		movimiento.almacen = almacen
		movimiento.fecha_operacion=fecha
		movimiento.numero = numero
		movimiento.usuario = request.user.usuario
		movimiento.save()
		for i in range(cdetalles):
			id="tblDetalle_id_"+str(i+1)
			cant="tblDetalle_cantidad_"+str(i+1)
			prec="tblDetalle_precio_"+str(i+1)
			val="tblDetalle_valor_"+str(i+1)		
			id_suministro = request.POST[id]
			suministro = Suministro.objects.get(codigo=id_suministro)
			grupo_suministros = GrupoSuministros.objects.get(codigo=suministro.grupo_suministros.codigo)
			cantidad = Decimal(request.POST[cant])
			precio= Decimal(request.POST[prec])
			valor = Decimal(request.POST[val])
			detalle = DetalleMovimiento(nro_detalle=i+1,movimiento=movimiento,suministro=suministro)
			detalle.cantidad=cantidad
			detalle.precio=precio
			detalle.valor = valor
			detalle.save()
		#return HttpResponseRedirect(reverse('almacen:registrar_ingreso'))

	context = {'tipos_ingreso':tipos_ingreso,'almacenes':almacenes,'tipos_documento':tipos_documento}
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
	mov_ant = Movimiento.objects.filter(tipo_movimiento=tipo.id, almacen__zona=zona, fecha_operacion__year=anio,almacen__empresa=empresa).aggregate(Max('id_movimiento'))
	id_ant=mov_ant['id_movimiento__max']        
	if id_ant is None:
		aux = 1            
	else:
		aux=int(id_ant[-5:])+1
	correlativo = str(aux).zfill(5)
	codigo = str(empresa.codigo)+str(tipo.codigo)+str(anio)+str(zona.codigo)+correlativo
	return codigo

'''def obtener_codigo_orden(tipo, anio, mes, empresa):
	cursor = connection.cursor()
	query = "SELECT fn_getcodigoorden(%i,'%s','%s','%s')" % (tipo, anio, mes, empresa)
	cursor.execute(query)
	row = cursor.fetchone()
	return row[0]'''

def upload_file(request):
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			archivo = Archivo(docfile = request.FILES['docfile'])			
			archivo.save(form)
			csv_filepathname="media/"+str(archivo.docfile)
			dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
			for fila in dataReader:
				cuenta = CuentaContable()
				cuenta.cuenta=fila[0]
				cuenta.descripcion=fila[1]
				cuenta.save()
			return HttpResponseRedirect(reverse('almacen:inicio'))
	else:
		form = UploadForm()
	return render(request, 'upload.html', {'form': form})

class Inicio(View):

	def get(self, request, *args, **kwargs):
		almacenes = Almacen.objects.all()
		if not almacenes:
			zonas = Zona.objects.all()
			if not zonas:
				return HttpResponseRedirect(reverse('almacen:crear_zona'))	 
			return HttpResponseRedirect(reverse('almacen:crear_almacen'))
		tipos_unidad = Tipo.objects.filter(tabla='tipo_unidad_medida')
		if not tipos_unidad:
			return HttpResponseRedirect(reverse('almacen:crear_tipo_unidad'))
		tipos_stock = Tipo.objects.filter(tabla='tipo_stock')
		if not tipos_stock:
			return HttpResponseRedirect(reverse('almacen:crear_tipo_stock'))
		cuentas = CuentaContable.objects.all()
		if not cuentas:
			return HttpResponseRedirect(reverse('almacen:upload_file'))
		grupos = GrupoSuministros.objects.all()
		if not grupos:
			return HttpResponseRedirect(reverse('almacen:crear_grupo_suministros'))
		suministros = Suministro.objects.all()	
		if not suministros:
			return HttpResponseRedirect(reverse('almacen:crear_suministro'))
		suministros_empresas = SuministroEmpresa.objects.all()
		if not suministros_empresas:
			return HttpResponseRedirect(reverse('almacen:registrar_inventario_inicial'))
		context = {'usuario': self.request.user}
		return render(request,'bienvenida.html', context)

class KardexSuministro(View):

	def get(self, request, *args, **kwargs):
		anios = Kardex.objects.datetimes('fecha_operacion', 'year')
		lista_anios = []
		for anio in anios:
			lista_anios.append(anio.year)
		meses = Kardex.objects.datetimes('fecha_operacion', 'month')
		lista_meses = []
		for mes in meses:
			lista_meses.append(mes.month)
		context = {'anios': lista_anios,'meses':lista_meses}
		return render(request,'kardex_suministro.html', context)

	def post(self, request, *args, **kwargs):
		mes = request.POST['meses']
		anio = request.POST['anios']
		cod_sumi = request.POST['codigo']
		suministro = Suministro.objects.get(codigo=cod_sumi)
		listado_kardex = Kardex.objects.filter(fecha_operacion__year=anio,fecha_operacion__month=mes,suministro=cod_sumi).order_by('suministro__descripcion','fecha_operacion','cantidads','fecha_registro')
		cantidade = listado_kardex.aggregate(Sum('cantidade'))
		cantidads = listado_kardex.aggregate(Sum('cantidads'))
		cantidadt = listado_kardex.aggregate(Sum('cantidadt'))
		valore = listado_kardex.aggregate(Sum('valore'))
		valors = listado_kardex.aggregate(Sum('valors'))
		valort = listado_kardex.aggregate(Sum('valort'))
		t_cantidad_e = cantidade['cantidade__sum']
		t_cantidad_s= cantidads['cantidads__sum']
		t_cantidad_t= cantidadt['cantidadt__sum']
		t_valor_e= valore['valore__sum']
		t_valor_s= valors['valors__sum']
		t_valor_t= valort['valort__sum']
		context = {'listado_kardex':listado_kardex,'mes':mes,'anio':anio,'suministro':suministro,'t_cantidad_e':t_cantidad_e,'t_cantidad_s':t_cantidad_s,'t_cantidad_t':t_cantidad_t,'t_valor_e':t_valor_e,'t_valor_s':t_valor_s,'t_valor_t':t_valor_t}
		return render(request, 'reporte_kardex_suministro.html', context)

class ReporteKardexSuministro(View):

	def get(self, request, *args, **kwargs):
		pass

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

class CrearTipoUnidad(FormView):
    template_name = 'tipo_unidad.html'
    form_class = TipoUnidadForm
    success_url = '/almacen'

    def form_valid(self, form):
    	form.save()
    	return super(CrearTipoUnidad, self).form_valid(form)    	

class CrearTipoStock(FormView):
    template_name = 'tipo_stock.html'
    form_class = TipoStockForm
    success_url = '/almacen'

    def form_valid(self, form):
    	form.save()
    	return super(CrearTipoStock, self).form_valid(form) 

class CrearAlmacen(FormView):
	template_name = 'almacen.html'
	form_class = AlmacenForm
	success_url = '/almacen/'

	def get_form(self, form_class):
		return form_class(self.request.user.empresa, **self.get_form_kwargs())

	def form_valid(self, form):
		form.save()
		return super(CrearAlmacen, self).form_valid(form)

class CrearZona(FormView):
    template_name = 'zona.html'
    form_class = ZonaForm
    success_url = '/almacen/'

    def form_valid(self, form):
    	form.save()
    	return super(CrearZona, self).form_valid(form)

class CrearSuministro(FormView):
    template_name = 'suministro.html'
    form_class = SuministroForm
    success_url = '/almacen/'

    def form_valid(self, form):
    	form.save()
    	return super(CrearSuministro, self).form_valid(form)  

class CrearGrupoSuministros(FormView):
    template_name = 'grupo_suministros.html'
    form_class = GrupoSuministrosForm
    success_url = '/almacen/'

    def form_valid(self, form):
    	form.save()
    	return super(CrearGrupoSuministros, self).form_valid(form)   

class ListadoSuministros(ListView):
	model = Suministro
	template_name = 'listado_suministros.html'
	context_object_name = 'suministros'
	paginate_by = 10
	queryset = Suministro.objects.filter(alta=True).order_by('codigo')

class DetalleSuministro(DetailView):
	model = Suministro
	template_name = 'detalle_suministro.html'

class ModificarSuministro(UpdateView):
	model = Suministro
	template_name = 'suministro_update_form.html'
	form_class = SuministroForm	
	success_url='/almacen/reporte_suministros'