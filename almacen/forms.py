from django import forms
from django.forms import ModelForm
from almacen.models import Tipo, Almacen, Zona, Suministro, GrupoSuministros
from usuarios.models import Empresa

class UploadForm(forms.Form):
    docfile = forms.FileField(label='Selecciona un archivo')

class TipoIngresoForm(forms.ModelForm):

    class Meta:
        model = Tipo
        fields =['codigo','descripcion_valor']

    def __init__(self, *args, **kwargs):
        self.tabla = "tipo_Ingreso"
        self.descripcion_campo = "tipo_Ingreso"
        super(TipoIngresoForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.tabla = self.tabla
        self.instance.descripcion_campo = self.descripcion_campo
        super(TipoIngresoForm, self).save(*args, **kwargs)

class TipoUnidadForm(forms.ModelForm):

    class Meta:
        model = Tipo
        fields =['codigo','descripcion_valor']

    def __init__(self, *args, **kwargs):
        self.tabla = "tipo_unidad_medida"
        self.descripcion_campo = "tipo_unidad_medida"
        super(TipoUnidadForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.tabla = self.tabla
        self.instance.descripcion_campo = self.descripcion_campo
        super(TipoUnidadForm, self).save(*args, **kwargs)        

class TipoStockForm(forms.ModelForm):

    class Meta:
        model = Tipo
        fields =['codigo','descripcion_valor']

    def __init__(self, *args, **kwargs):
        self.tabla = "tipo_stock"
        self.descripcion_campo = "tipo_stock"
        super(TipoStockForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.tabla = self.tabla
        self.instance.descripcion_campo = self.descripcion_campo
        super(TipoStockForm, self).save(*args, **kwargs)  

class AlmacenForm(forms.ModelForm):

    def __init__(self, empresa,*args, **kwargs):
        super(AlmacenForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].queryset = Empresa.objects.filter(codigo=empresa.codigo)        

    class Meta:
        model = Almacen
        fields =['descripcion','empresa','zona']

class ZonaForm(forms.ModelForm):

    class Meta:
        model = Zona
        fields =['descripcion']

class GrupoSuministrosForm(forms.ModelForm):

    class Meta:
        model = GrupoSuministros
        fields = ['descripcion','ctaalm','ctacomp']

        

class SuministroForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SuministroForm, self).__init__(*args, **kwargs)
        self.fields['tipo_unidad_medida'].queryset = Tipo.objects.filter(tabla="tipo_unidad_medida")
        self.fields['tipo_stock'].queryset = Tipo.objects.filter(tabla="tipo_stock")

    class Meta:
        model = Suministro
        fields =['descripcion', 'precio_mercado', 'grupo_suministros','tipo_unidad_medida','tipo_stock']        