from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from cart.models import Cart
from users.models import Shop_Users
from payments.models import Wallet

def create_order(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)

    cart = get_object_or_404(Cart, user=user)
    items = cart.items.all()

    if not items.exists():
        return redirect('cart:cart_view')

    active_order = Order.objects.filter(
        buyer=user,
        status__in=['PENDING', 'ACCEPTED']
    ).first()

    if active_order:
        return redirect('cart:cart_view')

    order = Order.objects.create(
        buyer=user,
        status='PENDING'
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            seller=item.product.owner,
            quantity=item.quantity,
            price=item.product.price, 
        )

    # items.delete()

    return redirect('cart:cart_view')


def seller_orders(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    seller = Shop_Users.objects.get(id=user_id)

    orders = Order.objects.filter(
        items__product__owner=seller
    ).distinct().order_by('-created_at')

    return render(
        request,
        'orders/orders.html',
        {
            'orders': orders,
            'user': user
        }
    )


def accept_order(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    for item in order.items.all():

        product = item.product

        if product.quantity < item.quantity:
            return redirect('orders:seller_orders')

        product.quantity -= item.quantity
        product.save()

    order.status = 'ACCEPTED'
    order.save()

    return redirect('orders:seller_orders')

def complete_order(request, order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    cart = get_object_or_404(Cart, user=user)
    items = cart.items.all()
    user_wallet = get_object_or_404(Wallet, user_id=user_id)    
    order = get_object_or_404(Order, id=order_id)
    order_item = get_object_or_404(OrderItem, id=order_id)

    if order.status != 'ACCEPTED':
        return redirect('cart:cart_view')
 
    order.status = 'COMPLETED'
    total_price = 0
    for item in order.items.all():
        total_price += item.price*order_item.quantity

    user_wallet.balance -= total_price
    user_wallet.save()
    order.save()
    items.delete()


    return redirect('cart:cart_view')