import chardet
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def parse_emails(file_stream, filename):
    """
    Считывает все строки из file_stream, пытается определить кодировку
    и возвращает список email (одна строка — один email).
    """
    raw = file_stream.read()
    # Попытка определить кодировку
    result = chardet.detect(raw)
    encoding = result['encoding'] or 'utf-8'
    try:
        text = raw.decode(encoding, errors='ignore')
    except (LookupError, UnicodeDecodeError):
        # на случай неизвестной кодировки
        text = raw.decode('utf-8', errors='ignore')
    
    lines = text.splitlines()
    emails = []
    for line in lines:
        line = line.strip()
        if line and EMAIL_REGEX.match(line):
            emails.append(line)
    return emails
