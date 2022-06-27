from django.core.exceptions import ValidationError


def validate_class_letter(value: str):
    if not value.isalpha():
        raise ValidationError('Invalid class letter: %s' % value, params={'class_letter': value})
