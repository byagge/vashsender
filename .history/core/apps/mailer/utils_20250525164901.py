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
    Возвращаем **все** непустые строки из файла.
    Классификация будет уже в classify_email.
    """
    raw = file_stream.read()
    try:
        text = raw.decode('utf-8', errors='ignore')
    except AttributeError:
        text = raw if isinstance(raw, str) else raw.decode('utf-8', errors='ignore')

    lines = text.splitlines()
    # Берём **все** непустые, без фильтра по EMAIL_REGEX
    return [line.strip() for line in lines if line.strip()]


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
