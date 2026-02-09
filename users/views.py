from .models import Shop_Users
from payments.models import Wallet
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def user_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        country = request.POST.get('country')

        if Shop_Users.objects.filter(email=email).exists():
            messages.error(request, "Користувач з таким email вже існує")
        else:
            user = Shop_Users(
                name=name,
                email=email,
                password=password,
                phone=phone,
                city=city,
                country=country
            )
            user.save()
            messages.success(request, "Користувача створено! Тепер увійдіть.")
            return redirect('login')

    return render(request, 'users/register.html')


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Shop_Users.objects.get(email=email)
            if user.password == password:  
                request.session['user_id'] = user.id  
                return redirect('profile')
            else:
                messages.error(request, "Неправильний пароль")
        except Shop_Users.DoesNotExist:
            messages.error(request, "Користувача не знайдено")

    return render(request, 'users/login.html')

def user_profile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)
    wallet = Wallet.objects.filter(user=user).first()

    return render(
        request,
        'users/profile.html',
        {
            'user': user,
            'wallet': wallet,
        }
        )