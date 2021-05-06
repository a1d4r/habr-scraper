import string

cyrillic_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
valid_chars = frozenset(
    '-_.() ' + string.ascii_letters + string.digits + cyrillic_letters
)


def to_valid_filename(s: str) -> str:
    return ''.join(c for c in s if c in valid_chars)
