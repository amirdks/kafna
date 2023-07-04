import re

from django.core.exceptions import ValidationError


def iran_phone_number_validator(value):
    regex = r'^(098|0098|98|\+98|0)?9(0[0-5]|[1 3]\d|2[0-3]|9[0-9]|41)\d{7}$'
    res = re.search(r'\bis\b', value)
    if res:
        return value
    raise ValidationError("شماره موبایل معتبر نمیباشد")
