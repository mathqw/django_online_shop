from django.shortcuts import render, redirect, get_object_or_404
from .forms import DepositForm, CardForm
from .models import Wallet, Card
from users.models import Shop_Users
from django.contrib import messages

# Create your views here.
def add_card(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = Shop_Users.objects.get(id=user_id)

    if request.method == 'POST':
        form = CardForm(request.POST)

        if form.is_valid():
            form.save(user=user)
            return redirect('profile')  

    else:
        form = CardForm()

    return render(request, 'payments/add_card.html', {
        'form': form,
        'user': user
    })

def deposit_to_wallet(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(Shop_Users, id=user_id)
    wallet, _ = Wallet.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = DepositForm(user, request.POST)
        if form.is_valid():
            card = form.cleaned_data['card']
            amount = form.cleaned_data['amount']

            card.balance -= amount  
            card.save()

            wallet.balance += amount
            wallet.save()

            messages.success(request, f"Гаманець поповнено на {amount} грн!")
            return redirect('profile')

    else:
        form = DepositForm(user)

    return render(request, 'payments/deposit.html', {
        'form': form,
        'user': user,
    })