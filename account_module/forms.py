from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from account_module.validaotrs import iran_phone_number_validator
from quiz_module.models import InternSubscription, JobSeekerSubscription
from quiz_module.validators import is_valid_iran_code

User = get_user_model()


class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=255, label='نام و نام خانوادگی *',
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    national_code = forms.CharField(max_length=255, label='کدملی * ',
                                    widget=forms.TextInput(attrs={"class": "form-control"}))
    # phone_number = forms.CharField(max_length=255, label='شماره تلفن همراه * ', widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=255, label='رمز عبور اکانت * ',
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

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


class JobSeekerRegisterEditForm(forms.ModelForm):
    class Meta:
        model = JobSeekerSubscription
        exclude = ["user", "created_at", "updated_at"]
        widgets = {
            "university_name": forms.TextInput(attrs={"class": "form-control"}),
            "field_of_study": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "fields": forms.SelectMultiple(attrs={"class": "form-select"}),
            "image_file": forms.FileInput(attrs={"class": "form-control-file", "accept": ".pdf"}),
        }
        help_texts = {
            "image_file": "فقط با فرمت pdf *",
        }
        labels = {
            "university_name": "نام دانشگاه",
            "field_of_study": "رشته تحصیلی",
            "email": "آدرس ایمیل",
            "image_file": "فایل تصویر",
        }


class InternRegisterEditForm(forms.ModelForm):
    class Meta:
        model = InternSubscription
        exclude = ["user", "created_at", "updated_at"]
        widgets = {
            "birthday": forms.TextInput(
                attrs={'class': 'form-control', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'}),
            "educational_field": forms.Select(attrs={"class": "form-select"}),
            "student_code": forms.TextInput(attrs={"class": "form-control"}),
            "school_name": forms.TextInput(attrs={"class": "form-control"}),
            "educational_stage": forms.Select(attrs={"class": "form-select"}),
            "parent_phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "fields": forms.SelectMultiple(attrs={"class": "form-select"}),
            "image_file": forms.FileInput(attrs={"class": "form-control-file", "accept": ".pdf"}),
        }
        help_texts = {
            "image_file": "فقط با فرمت pdf *",
        }
        labels = {
            "birthday": "تاریخ تولد",
            "educational_field": "نوع مرکز آموزشی",
            "student_code": "کد دانش آموزی",
            "school_name": "نام مدرسه",
            "educational_stage": "مقطع تحصیلی",
            "parent_phone_number": "شماره تلفن یکی از والدین",
            "email": "ایمیل",
            "image_file": "فایل تصویر",
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                   label="رمز عبور فعلی")
    new_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                   label="رمز عبور جدید")


class ForgetPasswordForm(forms.Form):
    new_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                   label="رمز عبور جدید")
    re_new_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                   label="تکرار رمز عبور جدید")

    def clean_re_new_password(self):
        re_new_password = self.cleaned_data.get("re_new_password")
        new_password = self.cleaned_data.get("new_password")
        if re_new_password == new_password:
            return re_new_password
        else:
            raise forms.ValidationError("کلمه عبور با تکرار کلمه عبور یکی نیست")
