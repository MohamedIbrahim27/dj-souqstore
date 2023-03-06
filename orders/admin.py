from django.contrib import admin

# Register your models here.
from.models import Order,OrderDetails,Checkout

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('user','is_finished',)

class OrderDetailsAdmin(admin.ModelAdmin):
    readonly_fields = ('product','order',)

class CheckoutAdmin(admin.ModelAdmin):
    readonly_fields = ('order',)
    

    
    
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderDetails,OrderDetailsAdmin)
admin.site.register(Checkout,CheckoutAdmin)