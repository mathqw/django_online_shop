from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ProductCreateForm
from users.models import Shop_Users
from .models import Product

def add_product(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)

    if request.method == 'POST':
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = user
            product.save()
            return redirect('profile')
    else:
        form = ProductCreateForm()

    return render(request, 'shops/add_product.html', {
        'form': form
    })

def my_products(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)

    products = Product.objects.filter(owner=user)

    return render(
        request,
        'shops/my_products.html',
        {
            'user': user,
            'products': products,
        }
    )