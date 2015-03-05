from django import forms
from django.forms import ModelForm
from almacen.models import Tipo, Almacen, Zona
from usuarios.models import Empresa

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

class AlmacenForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AlmacenForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].queryset = Empresa.objects.filter(codigo='001')        

    class Meta:
        model = Almacen
        fields =['descripcion','empresa','zona']

class ZonaForm(forms.ModelForm):

    class Meta:
        model = Zona
        fields =['descripcion']