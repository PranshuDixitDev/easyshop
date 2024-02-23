from django.contrib import admin
from orders.models import Payment, OrderDetails, OrderProduct
# Register your models here.


admin.site.register(Payment)
admin.site.register(OrderDetails)
admin.site.register(OrderProduct)
