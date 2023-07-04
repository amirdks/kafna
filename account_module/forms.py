from django import forms


class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=255, label='', widget=forms.TextInput(attrs={"class": "form-control"}))
    national_code = forms.CharField(max_length=255, label='', widget=forms.TextInput(attrs={"class": "form-control"}))
    phone_number = forms.CharField(max_length=255, label='', widget=forms.TextInput(attrs={"class": "form-control"}))
