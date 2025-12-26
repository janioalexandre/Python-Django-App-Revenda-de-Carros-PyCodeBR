from django.contrib import admin
from cars.models import Brand, Car, CarInventory

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class CarAdmin(admin.ModelAdmin):

    def formatted_value(self, obj):
        if obj.value is not None:
            valor = f"{obj.value:,.2f}"      # 510,000.00
            valor = valor.replace(",", "X").replace(".", ",").replace("X", ".")
            return f"R$ {valor}"
        return "-"

    formatted_value.short_description = "Valor (R$)"

    list_display = (
        'model',
        'brand',
        'factory_year',
        'model_year',
        'formatted_value',
    )

class CarInventoryAdmin(admin.ModelAdmin):

    def formatted_cars_value(self, obj):
        if obj.cars_value is None:
            return "-"

        valor = round(obj.cars_value, 2)
        valor = f"{valor:,.2f}"          # 510,000.00
        valor = valor.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {valor}"

    formatted_cars_value.short_description = "Valor total (R$)"
    formatted_cars_value.admin_order_field = 'cars_value'

    list_display = (
        'cars_count',
        'formatted_cars_value',
        'created_at',
    )

    search_fields = ('cars_count',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarInventory, CarInventoryAdmin)
