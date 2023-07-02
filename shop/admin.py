from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(City)
admin.site.register(Inventory)
admin.site.register(Supplier)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(InventoryProduct)


# Register your models here.
