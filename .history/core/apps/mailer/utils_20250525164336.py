import re
import dns.resolver
from .models import Contact
import requests

# Регулярка для синтаксиса e-mail
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Загрузка временных email-доменов с GitHub
url = "https://raw.githubusercontent.com/disposable/disposable-email-domains/master/domains.txt"
response = requests.get(url)

if response.status_code == 200:
    DISPOSABLE_DOMAINS = set(
        line.strip().lower() for line in response.text.splitlines() if line.strip()
    )
    print(f"{len(DISPOSABLE_DOMAINS)} доменов загружено.")
else:
    print("Не удалось загрузить список.")
    DISPOSABLE_DOMAINS = set()

def parse_emails(file_stream, filename=None):
    """
    Принимает загруженный файл (file_stream), читает его содержимое
    и возвращает список e-mail’ов (по одной строке — один e-mail).
    Игнорирует пустые и синтаксически неверные строки.
    """
    raw = file_stream.read()
    try:
        text = raw.decode('utf-8', errors='ignore')
    except AttributeError:
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
    """
    if not is_syntax_valid(email):
        return Contact.INVALID

    domain = email.split('@', 1)[1].lower()
    if domain in DISPOSABLE_DOMAINS:
        return Contact.BLACKLIST

    if not has_mx_record(domain):
        return Contact.INVALID

    return Contact.VALID
