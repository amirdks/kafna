import re


def phone_number_validator(value):
    regex = re.compile(r'^(098|0098|98|\+98|0)?9(0[0-5]|[1 3]\d|2[0-3]|9[0-9]|41)\d{7}$')
    result = re.search(regex, str(value))
    if not result:
        raise ValueError("شماره تلفن شما معتبر نمیباشد")
