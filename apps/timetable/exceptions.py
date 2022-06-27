from django.core.exceptions import ValidationError


def validate_class_grade(value: int) -> None:
    if value not in range(7, 13):
        raise ValidationError('Invalid class grade: %s' % value)
