from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailBackend(ModelBackend):
    """
    Аутентификация по email, не блокируя вход для неактивных (is_active=False).
    Проверяем пароль, но игнорируем флаг is_active.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username or kwargs.get('email')
        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def user_can_authenticate(self, user):
        # Разрешаем вход даже если is_active=False
        return True