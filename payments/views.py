from django.shortcuts import render, redirect
from .forms import CardForm
from users.models import Shop_Users

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