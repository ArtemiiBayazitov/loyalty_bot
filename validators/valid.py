import re
from datetime import datetime


def is_valid_phone(phone):
    return re.match(r'^(\+7|8)\d{10}$', phone) is not None


def is_valid_birthday(text) -> bool:
    try:
        date = datetime.strptime(text, "%d.%m.%Y").date()
        if date.year < 1900 or date >= datetime.now().date():
            return False
        return True
    except ValueError:
        return False