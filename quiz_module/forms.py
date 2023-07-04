from django import forms

from quiz_module.models import QuizSubscription


class RegisterQuizForm(forms.ModelForm):
    class Meta:
        model = QuizSubscription
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
