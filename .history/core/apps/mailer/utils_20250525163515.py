import re
import dns.resolver
from .models import Contact
import requests

# Регулярка для синтаксиса e-mail
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Определение «чёрных» доменов (например, временные почты)
DISPOSABLE_DOMAINS = {
    "mailinator.com",
    "tempmail.com",
    "trashmail.com",
    "10minutemail.com",
    # … добавьте другие при необходимости …
}

def parse_emails(file_stream, filename=None):
    """
    Принимает загруженный файл (file_stream), читает его содержимое
    и возвращает список e-mail’ов (по одной строке — один e-mail).
    Игнорирует пустые и синтаксически неверные строки.
    """
    raw = file_stream.read()
    # Попробуем декодировать в utf-8 с игнорированием ошибок
    try:
        text = raw.decode('utf-8', errors='ignore')
    except AttributeError:
        # Если raw уже str
        text = raw if isinstance(raw, str) else raw.decode('utf-8', errors='ignore')

    lines = text.splitlines()
    emails = []
    for line in lines:
        e = line.strip()
        if e and EMAIL_REGEX.match(e):
            emails.append(e)
    return emails

def is_syntax_valid(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))

def has_mx_record(domain: str) -> bool:
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except Exception:
        return False

def classify_email(email: str) -> str:
    """
    Классифицирует email в один из трёх статусов:
      - Contact.INVALID
      - Contact.BLACKLIST
      - Contact.VALID
    Логика:
      1) Синтаксис
      2) Чёрный список доменов
      3) MX-запись
      4) По умолчанию — VALID
    """
    # 1) синтаксис
    if not is_syntax_valid(email):
        return Contact.INVALID

    # 2) disposable домены
    domain = email.split('@', 1)[1].lower()
    if domain in DISPOSABLE_DOMAINS:
        return Contact.BLACKLIST

    # 3) MX-запись
    if not has_mx_record(domain):
        return Contact.INVALID

    # 4) всё ок
    return Contact.VALID
