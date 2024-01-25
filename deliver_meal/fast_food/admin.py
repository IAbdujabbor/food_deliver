from django.contrib import admin

from fast_food.models import *

# Register your models here.
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(Shipment)
