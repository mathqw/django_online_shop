from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductCreateForm
from users.models import Shop_Users
from .models import Product

def add_product(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)

    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = user
            product.is_active = request.POST.get('is_active') == '1'
            product.save()
            return redirect('my_products')
    else:
        form = ProductCreateForm()

    return render(request, 'shops/add_product.html', {
        'form': form,
        'user': user,
        'page_title': 'Додати товар',
    })

def my_products(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)

    products = Product.objects.filter(owner=user).select_related('category')

    return render(
        request,
        'shops/my_products.html',
        {
            'user': user,
            'products': products,
        }
    )

def delete_product(request, product_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)

    product = get_object_or_404(Product, id=product_id, owner=user)

    if request.method == "POST":
        product.delete()
        return redirect('my_products')

    return redirect('my_products')

def toggle_product_active(request, product_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)

    product = get_object_or_404(Product, id=product_id, owner=user)

    if request.method == "POST":
        product.is_active = not product.is_active
        product.save()

    return redirect('my_products')