from django import forms

from quiz_module.models import InternSubscription, InternField, JobSeekerField, JobSeekerSubscription


class RegisterQuizForm(forms.ModelForm):
    class Meta:
        model = InternSubscription
        exclude = ["user", "created_at", "updated_at"]
        widgets = {
            "field": forms.Select(attrs={"class": "form-control"}),
            "field_2": forms.Select(attrs={"class": "form-control"}),
            "field_3": forms.Select(attrs={"class": "form-control"}),
            "image_file": forms.FileInput(attrs={"class": "form-control-file", "accept": ".pdf"}),
        }
        help_texts = {
            "field": "این فیلد الزامی است",
            "field_2": "میتوانید خالی بگذارید",
            "field_3": "میتوانید خالی بگذارید",
        }
        labels = {
            "field": "انتخاب رشته اول * ",
            "field_2": "انتخاب رشته دوم",
            "field_3": "انتخاب رشته سوم",
            "image_file": "آپلود عکس * ",
        }


class JobSeekerRegisterForm(forms.ModelForm):
    class Meta:
        model = JobSeekerSubscription
        exclude = ["user", "fields", "created_at", "updated_at"]
        widgets = {
            "university_name": forms.TextInput(attrs={"class": "form-control"}),
            "field_of_study": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
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



class InternRegisterForm(forms.ModelForm):
    class Meta:
        model = InternSubscription
        exclude = ["user", "fields", "created_at", "updated_at"]
        widgets = {
            "birthday": forms.TextInput(
                attrs={'class': 'form-control', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'}),
            "educational_field": forms.Select(attrs={"class": "form-select"}),
            "student_code": forms.TextInput(attrs={"class": "form-control"}),
            "school_name": forms.TextInput(attrs={"class": "form-control"}),
            "educational_stage": forms.Select(attrs={"class": "form-select"}),
            "parent_phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
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


class SubmitPhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=255, label='شماره تلفن همراه * ',
                                   widget=forms.TextInput(attrs={"class": "form-control"}))


class InternFieldForm(forms.Form):
    fields = forms.ModelMultipleChoiceField(queryset=InternField.objects.all(), label="انتخاب رشته ها",
                                            widget=forms.SelectMultiple(attrs={"class": "form-select"}))


class JobSeekerFieldForm(forms.Form):
    fields = forms.ModelMultipleChoiceField(queryset=JobSeekerField.objects.all(), label="انتخاب رشته ها",
                                            widget=forms.SelectMultiple(attrs={"class": "form-select"}))
