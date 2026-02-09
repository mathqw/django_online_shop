from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Перевіряє, чи користувач залогінений.
    Якщо ні — редіректить на сторінку логіну.
    Не перевіряє сторінки: login, register, admin
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = [
            reverse('login'),     
            reverse('register'),   
            '/admin/',            
        ]

        if not request.user.is_authenticated:
            if request.path not in excluded_paths and not request.path.startswith('/admin/'):
                return redirect('login')

        response = self.get_response(request)
        return response

