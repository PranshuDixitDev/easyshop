from django import forms
from orders.models import OrderDetails
from .forms import OrderDetails


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderDetails
        fields = ['first_name', 'last_name', 'phone' ,
                'email', 'address_line_1', 'address_line_2',
                'country', 'state', 'city', 'order_note']