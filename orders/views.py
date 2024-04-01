from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import OrderDetails, Payment, OrderProduct
import datetime
import json
# Create your views here.


def payments(request):
    body = json.loads(request.body)
    orderedtails = OrderDetails.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # store transaction details on payment model 
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_field = body["payment_field"],
        amount_paid = orderedtails.order_total,
        status = body['status']
    )
    payment.save()
    
    orderedtails.payment = payment
    orderedtails.is_ordered = True
    orderedtails.save()
    
    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)
    
    for item in cart_items:
        orderProduct = OrderProduct()
        orderProduct.order = order.id
        orderProduct.payment = payment
        orderProduct.user = request.user.id
        orderProduct.product_id = item.product_id
        orderProduct.quantity = item.quantity
        orderProduct.product_price = item.product.price
        orderProduct.ordered = True
        orderProduct.save()
        # orderProduct.variation = item.variations
        
    
    #Reduce the quantity of rhe sold products
    
    
    # Clear the Cart 
    
    
    # Send order recevied email to customer 
    
    
    # Send order number and transaction id back to snedData method via json response. 
    
    return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0,):
    current_user = request.user
    
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = (18 * total)/100
    grand_total = total + tax
    
    
    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = OrderDetails()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Genrate Order Number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            
            data.order_number = order_number
            
            data.save()
            
            orderdetails = OrderDetails.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'orderdetails': orderdetails,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total, 
                
            }
            return render(request, 'orders/payments.html', context)
        
        else:
            return redirect('checkout')