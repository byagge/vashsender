# core/apps/mailer/utils.py
import re
import dns.resolver
from .models import Contact

# Простая проверка синтаксиса
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Набор «чёрных» доменов (пример; расширьте по необходимости)
DISPOSABLE_DOMAINS = {
    "mailinator.com", "tempmail.com", "trashmail.com", "10minutemail.com",
    # ... добавьте сюда свои, или загрузите из файла ...
}

def is_syntax_valid(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))

def has_mx_record(domain: str) -> bool:
    try:
        # попробуем найти MX-запись
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except Exception:
        return False

def classify_email(email: str) -> str:
    """
    Возвращает один из статусов Contact.VALID, Contact.INVALID, Contact.BLACKLIST.
    Логика:
      1) Синтаксис
      2) Чёрный список доменов (DISPOSABLE_DOMAINS)
      3) MX-запись
    """
    # 1. синтаксис
    if not is_syntax_valid(email):
        return Contact.INVALID

    # 2. домен в локальном black-list?
    domain = email.split('@', 1)[1].lower()
    if domain in DISPOSABLE_DOMAINS:
        return Contact.BLACKLIST

    # 3. MX-запись
    if not has_mx_record(domain):
        return Contact.INVALID

    # иначе — считаем валидным
    return Contact.VALID
