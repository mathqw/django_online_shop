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
        # Сторінки, де не потрібна авторизація
        excluded_paths = [
            reverse('login'),      # твій URL name для логіну
            reverse('register'),   # твій URL name для реєстрації
            '/admin/',             # якщо є адмінка
        ]

        if not request.user.is_authenticated:
            if request.path not in excluded_paths and not request.path.startswith('/admin/'):
                return redirect('login')

        response = self.get_response(request)
        return response

