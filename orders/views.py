from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart

@login_required(login_url='/account/login/')
def view_orders(request):
    orders = Order.objects.filter(user = request.user)
    return render(request, 'orders/list.html', {'orders':orders})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
            cart.clear()
            return redirect('account:cabinet')
    else:
        if request.user.is_authenticated == True:
            form = OrderCreateForm(initial = {'first_name':request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email})
        else:
            form = OrderCreateForm()
    return render(request,'orders/create.html',{'cart': cart, 'form': form})
