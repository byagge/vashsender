import csv, io, json
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def parse_emails(file_stream, filename):
    content = file_stream.read().decode('utf-8')
    emails = []
    if filename.endswith('.json'):
        data = json.loads(content)
        for item in data:
            email = item.get('email') or item
            try:
                validate_email(email)
                emails.append(email)
            except ValidationError:
                continue
    else:
        sep = ',' if filename.endswith('.csv') else '\n'
        for line in content.split(sep):
            email = line.strip()
            try:
                validate_email(email)
                emails.append(email)
            except ValidationError:
                continue
    return set(emails)