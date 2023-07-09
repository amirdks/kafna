from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from account_module.validaotrs import iran_phone_number_validator
from quiz_module.validators import is_valid_iran_code

User = get_user_model()
class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=255, label='نام و نام خانوادگی *', widget=forms.TextInput(attrs={"class": "form-control"}))
    national_code = forms.CharField(max_length=255, label='کدملی * ', widget=forms.TextInput(attrs={"class": "form-control"}))
    # phone_number = forms.CharField(max_length=255, label='شماره تلفن همراه * ', widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=255, label='رمز عبور اکانت * ', widget=forms.PasswordInput(attrs={"class": "form-control"}))

    # def clean_phone_number(self):
    #     phone_number = self.cleaned_data.get("phone_number")
    #     try:
    #         iran_phone_number_validator(phone_number)
    #     except ValidationError as e:
    #         raise forms.ValidationError(e)
    #     return phone_number

    def clean_national_code(self):
        national_code = self.cleaned_data.get("national_code")
        print(national_code)
        duplicated_user = User.objects.filter(national_code__exact=national_code).exists()
        print(duplicated_user)
        if duplicated_user:
            raise forms.ValidationError("کاربری با این کد ملی از قبل وجود دارد")
        try:
            is_valid_iran_code(national_code)
        except ValidationError as e:
            raise forms.ValidationError(e)
        return national_code

