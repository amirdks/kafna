from django import forms

from quiz_module.models import Quiz


class RegisterQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ["created_at", "updated_at"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "national_code": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
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
            "full_name": "نام و نام خانوادگی * ",
            "national_code": "کدملی * ",
            "phone_number": "شماره تلفن همراه * ",
            "field": "انتخاب رشته اول * ",
            "field_2": "انتخاب رشته دوم",
            "field_3": "انتخاب رشته سوم",
            "image_file": "آپلود عکس * ",
        }
