from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
@admin.register(Cata)
class userCata(ImportExportModelAdmin):
     import_id_fields = ['id', 'name', 'slug', 'price', 'digital', 'image', 'category', 'description', 'date', 'duration', 'location']


@admin.register(Vino)
class userVino(ImportExportModelAdmin):
     import_id_fields = ['id', 'name', 'slug', 'price', 'digital', 'image', 'category', 'description', 'bodega','grapes','denomiation','crianza','tipo']

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)





