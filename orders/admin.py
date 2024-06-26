from django.contrib import admin
from orders.models import Payment, OrderDetails, OrderProduct
# Register your models here.




class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'city',
                    'order_total', 'tax', 'status', 'is_ordered',
                    'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]
    
    
admin.site.register(Payment)
admin.site.register(OrderDetails, OrderAdmin)
admin.site.register(OrderProduct)
