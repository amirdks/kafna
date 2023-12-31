from django import template
from django.template.defaultfilters import stringfilter
from django.urls import reverse
from django.utils.safestring import mark_safe
from jalali_date import date2jalali, datetime2jalali

register = template.Library()


def persian_numbers(my_str):
    numbers = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }

    for e, p in numbers.items():
        my_str = str(my_str).replace(e, p)
    return my_str


@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')


# @register.filter(name='show_jalali_date')
# def show_jalali_date(value):
#     return date2jalali(value)


@register.filter(name='three_digits_currency')
def three_digits_currency(value):
    if not value == "رایگان":
        return '{:,}'.format(value) + ' تومان'
    return value


@register.simple_tag
def multiply(quantity, price, *args, **kwargs):
    return three_digits_currency(quantity * price)


@register.filter(name='show_detail')
def show_detail(product, num):
    details = [
        'size', 'weight', 'screen_size', 'cpu',
        'gpu', 'camera_resolution', 'software', 'battery',
        'release_date'
    ]
    return eval(f'product.{details[int(num)]}')


@register.filter(name='show_persian_detail')
def show_persian_detail(product, num):
    persian_details = ['سایز', 'وزن', 'سایز صفحه نمایش', 'پردازنده', 'پردازنده گرافیکی', 'کیفیت دوربین', 'سیستم عامل',
                       'باطری', 'تاریخ عرضه']
    return persian_details[int(num)]


@register.filter(name='commend_mode')
def commend_mode(commend_mode):
    if commend_mode == 'Bad':
        return mark_safe('<i class="fa-solid fa-thumbs-down"></i>')
    elif commend_mode == 'Good':
        return mark_safe('<i class="fa-solid fa-thumbs-up"></i>')
    else:
        return mark_safe('<i class="fa-solid fa-face-meh"></i>')


@register.filter(name='change_month')
def change_month(date):
    jmonth = {
        "01": "فروردین",
        "02": "اردیبهشت",
        "03": "خرداد",
        "04": "تیر",
        "05": "مرداد",
        "06": "شهریور",
        "07": "مهر",
        "08": "آبان",
        "09": "آذر",
        "10": "دی",
        "11": "بهمن",
        "12": "اسفند",
    }
    date = str(date).replace("-", " ")
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    for e, p in jmonth.items():
        month = month.replace(e, p)
    return f"{day} {month} {year}"


# @register.filter(name='show_jalali_date')
# def show_jalali_date(value):
#     return date2jalali(value)
#
#
# @register.filter(name='show_jalali_date_time')
# def show_jalali_date_time(value):
#     return datetime2jalali(value)

@register.filter(name='custom_slice')
def custom_slice(text, num):
    sliced_text = text[:int(num)]
    if len(sliced_text) < len(text):
        return sliced_text + "..."
    else:
        return text


@register.filter(name='generate_validity_duration')
def generate_validity_duration(month):
    validity_duration_dict = {
        "1": "یک ماهه",
        "3": "سه ماهه",
        "6": "شش ماهه",
        "12": "دوازده ماهه",
    }
    return validity_duration_dict[month]


@register.filter(name='dont_show_none')
def dont_show_none(value):
    if value is None or not value:
        return '____'
    return value


@register.filter(name='show_jalali_date')
def show_jalali_date(value):
    return date2jalali(value)


@register.filter(name='show_jalali_date_time')
def show_jalali_date_time(value):
    return datetime2jalali(value)


@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)


@register.simple_tag
def persian_number_converter(my_str):
    return persian_numbers(my_str)


@register.filter(name='persian_number_converter')
def persian_number_converter(my_str):
    return persian_numbers(my_str)


@register.filter(name='generate_persian')
def generate_persian(my_str: str):
    my_obj = {
        "hs": "دبیرستان",
        "vs": "هنرستان",
        "tenth": "دهم",
        "eleventh": "یازدهم",
        "twelfth": "دوازدهم",
    }
    return my_obj[my_str.lower()]
