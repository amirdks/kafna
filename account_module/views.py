from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from account_module.forms import JobSeekerRegisterEditForm, InternRegisterEditForm, ChangePasswordForm
from quiz_module.models import QuizAnswer, InternSubscription, JobSeekerSubscription
from utils.send_email import Util


# Create your views here.
class UserPanelView(LoginRequiredMixin, View):
    def get(self, request):
        # answers = QuizAnswer.objects.filter(user_id=request.user.id)
        context = {
        }
        return render(request, 'account_module/user_panel.html', context)


class UserPanelRegisterDetailView(LoginRequiredMixin, View):
    def get(self, request):
        jobseeker = None
        intern = None
        try:
            intern = InternSubscription.objects.get(user_id=request.user.id)
        except InternSubscription.DoesNotExist:
            jobseeker = JobSeekerSubscription.objects.filter(user_id=request.user.id)
            if jobseeker.exists():
                jobseeker = jobseeker.first()
        context = {
            "intern": intern,
            "jobseeker": jobseeker
        }
        return render(request, 'account_module/register_detail.html', context)


class UserPanelRegisterEditView(LoginRequiredMixin, View):

    def get(self, request):
        jobseeker = None
        intern = None
        form = None
        try:
            intern = InternSubscription.objects.get(user_id=request.user.id)
        except InternSubscription.DoesNotExist:
            jobseeker = JobSeekerSubscription.objects.filter(user_id=request.user.id)
            if jobseeker.exists():
                jobseeker = jobseeker.first()
        if jobseeker:
            form = JobSeekerRegisterEditForm(instance=jobseeker)
        elif intern:
            form = InternRegisterEditForm(instance=intern)
        context = {
            "form": form,
        }
        return render(request, 'account_module/register_edit.html', context)

    def post(self, request):
        jobseeker = None
        intern = None
        form = None
        try:
            intern = InternSubscription.objects.get(user_id=request.user.id)
        except InternSubscription.DoesNotExist:
            jobseeker = JobSeekerSubscription.objects.filter(user_id=request.user.id)
            if jobseeker.exists():
                jobseeker = jobseeker.first()
        if jobseeker:
            form = JobSeekerRegisterEditForm(request.POST, request.FILES, instance=jobseeker)
        elif intern:
            form = InternRegisterEditForm(request.POST, request.FILES, instance=intern)

        if form.is_valid():
            instance = form.save()
            Util.send_email({"email_subject": "ثبت نام کارآموز جدید", "email_body":
                f"کاربر به اسم {instance.user.full_name} و شماره تلفن {instance.user.phone_number} و کد ملی {instance.user.national_code}اطالاعات خود را ویرایش کرد",
                             "to_email": ["kataunasgari@gmail.com", "jalilimba@gmail.com",
                                          "amirhossein6168@gmail.com"]})
            return redirect(reverse("user_panel_register_detail_view"))
        context = {
            "form": form,
        }
        return render(request, 'account_module/register_edit.html', context)


class UserChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangePasswordForm()
        context = {
            "form": form
        }
        return render(request, 'account_module/user_change_password.html', context)

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        user = request.user
        if form.is_valid():
            old_pass = form.cleaned_data.get("old_password")
            new_pass = form.cleaned_data.get("new_password")
            if user.check_password(old_pass):
                user.set_password(new_pass)
                user.save()
                login(request, user)
                return redirect(reverse("user_panel_view"))
            else:
                form.add_error("old_password", "رمز عبور فعلی درست نیست")
        context = {
            "form": form
        }
        return render(request, 'account_module/user_change_password.html', context)
