from django.db import models
from django.db.models import Max
from usuarios.models import Empresa

class Zona(models.Model):
    codigo = models.CharField(primary_key=True,max_length=3)
    descripcion = models.CharField(max_length=30)

    def save(self):
        zona_ant = Zona.objects.all().aggregate(Max('codigo'))
        cod_ant=zona_ant['codigo__max']        
        if cod_ant is None:
            aux = 1            
        else:
            aux=int(cod_ant)+1
        self.codigo=str(aux).zfill(3) 
        super(Zona, self).save()

    def __str__(self):
        return self.descripcion

class Almacen(models.Model):
    descripcion = models.CharField(max_length=30)
    empresa = models.ForeignKey(Empresa)
    zona = models.ForeignKey(Zona)

    def __str__(self):
        return self.descripcion

class CuentaContable(models.Model):
    cuenta = models.CharField(primary_key=True,max_length=10)
    descripcion = models.CharField(max_length=150)
    
    def __str__(self):
        return self.cuenta

class Tipo(models.Model):
    tabla = models.CharField(max_length=25)
    descripcion_campo = models.CharField(max_length=25)
    codigo = models.CharField(max_length=10)
    descripcion_valor = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.descripcion_valor

class GrupoSuministros(models.Model):
    codigo = models.CharField(primary_key=True,max_length=10)
    descripcion = models.CharField(max_length=100)
    alta = models.BooleanField(default=True)
    ctaalm = models.ForeignKey(CuentaContable, related_name="ctaalm")
    ctacomp = models.ForeignKey(CuentaContable, related_name="ctacomp")
    fecha_registro = models.DateTimeField(auto_now=True)

    def save(self):
        grupo_ant = GrupoSuministros.objects.all().aggregate(Max('codigo'))
        cod_ant=grupo_ant['codigo__max']        
        if cod_ant is None:
            aux = 1            
        else:
            aux=int(cod_ant)+1
        self.codigo=str(aux).zfill(10) 
        super(GrupoSuministros, self).save()

    def __str__(self):
        return self.descripcion

class Suministro(models.Model):
    codigo = models.CharField(primary_key=True, max_length=14)
    descripcion = models.CharField(max_length=100)
    alta = models.BooleanField(default=True)
    precio_mercado = models.DecimalField(max_digits=15, decimal_places=5)
    especificaciones = models.CharField(max_length=500, blank=True)
    grupo_suministros = models.ForeignKey(GrupoSuministros)
    tipo_unidad_medida = models.ForeignKey(Tipo, related_name="tipo_unidad_medida")
    tipo_stock = models.ForeignKey(Tipo, related_name="tipo_stock")
    fecha_registro = models.DateTimeField(auto_now=True)
    
    def save(self):
        sumi_ant = Suministro.objects.filter(grupo_suministros=self.grupo_suministros).aggregate(Max('codigo'))
        cod_ant=sumi_ant['codigo__max']        
        if cod_ant is None:
            self.codigo=self.grupo_suministros.codigo+'0001'
        else:
            aux=int(cod_ant)+1
            self.codigo=str(aux).zfill(14)
        super(Suministro, self).save()

    def __str__(self):
        return self.descripcion

class Movimiento(models.Model):
    id_movimiento = models.CharField(primary_key=True,max_length=16)
    tipo_movimiento = models.ForeignKey(Tipo, related_name="tipo_movimiento")
    tipo_ingreso = models.ForeignKey(Tipo, related_name="tipo_ingreso")
    tipo_documento = models.ForeignKey(Tipo, related_name="tipo_documento")
    serie = models.CharField(max_length=15, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    fecha_operacion = models.DateTimeField()
    almacen = models.ForeignKey(Almacen)
    observacion = models.CharField(max_length=800, blank=True)
    usuario = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.id_movimiento

class DetalleMovimiento(models.Model):
    nro_detalle = models.IntegerField()
    movimiento = models.ForeignKey(Movimiento)
    suministro = models.ForeignKey(Suministro)
    cantidad = models.DecimalField(max_digits=15, decimal_places=5)
    precio = models.DecimalField(max_digits=15, decimal_places=5)
    valor = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    
    class Meta:
        unique_together = (('nro_detalle', 'movimiento'),)

class Kardex(models.Model):
    correlativo = models.IntegerField()
    suministro = models.ForeignKey(Suministro)
    fecha_operacion = models.DateTimeField()
    cantidade = models.DecimalField(max_digits=15, decimal_places=5)
    precioe = models.DecimalField(max_digits=15, decimal_places=5)
    valore = models.DecimalField(max_digits=15, decimal_places=5)
    cantidads = models.DecimalField(max_digits=15, decimal_places=5)
    precios = models.DecimalField(max_digits=15, decimal_places=5)
    valors = models.DecimalField(max_digits=15, decimal_places=5)
    cantidadt = models.DecimalField(max_digits=15, decimal_places=5)
    preciot = models.DecimalField(max_digits=15, decimal_places=5)
    valort = models.DecimalField(max_digits=15, decimal_places=5)
    nrodetallemovimiento = models.IntegerField()
    id_movimiento = models.ForeignKey(Movimiento)
    fecha_registro = models.DateTimeField(auto_now=True)

class SuministroEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa)
    suministro = models.ForeignKey(Suministro)
    stock = models.DecimalField(max_digits=15, decimal_places=5)
    precio = models.DecimalField(max_digits=15, decimal_places=5)
    valor = models.DecimalField(max_digits=15, decimal_places=5)