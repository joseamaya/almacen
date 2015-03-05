from django import forms
from django.forms import ModelForm
from almacen.models import Tipo, Almacen

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

    class Meta:
        model = Almacen
        fields =['descripcion','empresa','zona']