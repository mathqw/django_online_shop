from .models import User
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

        # перевіряємо чи такий email вже існує
        if User.objects.filter(email=email).exists():
            messages.error(request, "Користувач з таким email вже існує")
        else:
            user = User(
                name=name,
                email=email,
                password=password,  # plain text
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
            user = User.objects.get(email=email)
            if user.password == password:  # порівнюємо plain text
                request.session['user_id'] = user.id  # авторизуємо через сесію
                return redirect('profile')
            else:
                messages.error(request, "Неправильний пароль")
        except User.DoesNotExist:
            messages.error(request, "Користувача не знайдено")

    return render(request, 'users/login.html')

def user_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    return render(request, 'users/profile.html', {"user": user})