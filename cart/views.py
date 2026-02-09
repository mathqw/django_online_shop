from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from users.models import Shop_Users
from shops.models import Product
from orders.models import Order

def cart_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = Shop_Users.objects.get(id=user_id)
    products = Product.objects.filter(is_active=True)\
        .select_related('category', 'owner')\
        .order_by('-created_at')
    
    active_order = Order.objects.filter(
    buyer=user,
    status__in=['PENDING', 'ACCEPTED']
    ).first()

    cart, _ = Cart.objects.get_or_create(user=user)
    return render(
        request,
        'cart/cart.html',
        {
            'user': user,
            'products': products,
            'cart': cart,
            'order': active_order,
        }
    )

def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect('cart:cart_view')

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)
    product = get_object_or_404(Product, id=product_id)

    cart, _ = Cart.objects.get_or_create(user=user)

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:
        item.quantity = quantity
    else:
        item.quantity += quantity  

    item.save()

    return redirect('cart:cart_view')


def remove_from_cart(request, item_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)
    cart = get_object_or_404(Cart, user=user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    item.delete()
    return redirect('cart:cart_view')