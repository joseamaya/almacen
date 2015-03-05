from django.contrib import admin

# Register your models here.
from almacen.models import Suministro,GrupoSuministros,CuentaContable,Tipo, Zona, Almacen

class SuministroAdmin(admin.ModelAdmin):
	ordering = ('descripcion',)
	fields = ('descripcion', 'precio_mercado', 'grupo_suministros','tipo_unidad_medida','tipo_stock', 'alta')

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "tipo_unidad_medida":
			kwargs["queryset"] = Tipo.objects.filter(tabla='tipo_unidad_medida')
		if db_field.name == "tipo_stock":
			kwargs["queryset"] = Tipo.objects.filter(tabla='tipo_stock')
		return super(SuministroAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class GrupoSuministrosAdmin(admin.ModelAdmin):
	ordering = ('descripcion',)
	fields = ('descripcion', 'ctaalm', 'ctacomp', 'alta')

class CuentaContableAdmin(admin.ModelAdmin):
	ordering = ('cuenta',)

class TipoAdmin(admin.ModelAdmin):
	ordering = ('tabla',)

admin.site.register(Suministro,SuministroAdmin)
admin.site.register(GrupoSuministros,GrupoSuministrosAdmin)
admin.site.register(CuentaContable,CuentaContableAdmin)
admin.site.register(Tipo,TipoAdmin)
admin.site.register(Zona)
admin.site.register(Almacen)