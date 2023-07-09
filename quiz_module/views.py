import json
import math

from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from account_module.forms import RegisterForm
from .form_errors import form_error
from .forms import JobSeekerRegisterForm, InternRegisterForm, InternFieldForm, JobSeekerFieldForm
from .models import Quiz, QuizQuestion, QuizAnswer, InternSubscription, JobSeekerSubscription

User = get_user_model()


# Create your views here.
class RegisterQuizView(View):
    def get(self, request):
        form = RegisterQuizForm()
        register_form = RegisterForm()
        context = {
            'form': form,
            'register_form': register_form,
        }
        return render(request, "quiz_module/register_quiz_page.html", context)

    def post(self, request):
        form = RegisterQuizForm(request.POST, request.FILES)
        register_form = RegisterForm(request.POST)
        if form.is_valid() and register_form.is_valid():
            full_name = register_form.cleaned_data.get("full_name")
            national_code = register_form.cleaned_data.get("national_code")
            phone_number = register_form.cleaned_data.get("phone_number")
            password = register_form.cleaned_data.get("password")
            new_user = User.objects.create_user(national_code, phone_number, password, full_name=full_name)
            login(request, new_user)
            quiz_subscription = form.save(commit=False)
            quiz_subscription.user = new_user
            quiz_subscription.save()
            return render(request, "quiz_module/quiz_success.html")
        error = form_error(form)
        context = {
            'form': form,
            'register_form': register_form,
        }
        return render(request, "quiz_module/register_quiz_page.html", context)


class TestView(TemplateView):
    template_name = 'quiz_module/quiz_success.html'


class QuizView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            user_quiz_subscription = InternSubscription.objects.get(user_id=request.user.id)
        except InternSubscription.DoesNotExist:
            raise Http404("لطفا ابتدا در آزمون شرکت کنید")
        field_1 = user_quiz_subscription.field
        field_2 = user_quiz_subscription.field_2
        field_3 = user_quiz_subscription.field_3
        quiz_1 = None
        quiz_2 = None
        quiz_3 = None
        try:
            quiz_1 = Quiz.objects.get(field_id=field_1.id)
            if field_2:
                quiz_2 = Quiz.objects.get(field_id=field_2.id)
            if field_3:
                quiz_3 = Quiz.objects.get(field_id=field_3.id)
        except Quiz.DoesNotExist:
            pass

        context = {
            "quiz_1": quiz_1,
            "quiz_2": quiz_2,
            "quiz_3": quiz_3,
        }
        return render(request, 'quiz_module/quiz_page.html', context)

    def post(self, request):
        answers = QuizAnswer.objects.filter(user_id=request.user.id)
        if answers.exists():
            return JsonResponse(
                {"status": "error", "message": "شما قبلا در آزمون شرکت کرده اید برای دیدن نتیجه برروی دکمه کلیک کنید"})
        json_data = request.POST.get("data")
        data = json.loads(json_data)
        result_message = ""
        for quiz in data:
            questions_number = 0
            answered_numbers = 0
            quiz_obj = Quiz.objects.prefetch_related("quizquestion_set").get(id=quiz.get("id"))
            questions_number += quiz_obj.quizquestion_set.count()
            for option in quiz.get("optionData"):
                option_obj = QuizQuestion.objects.get(id=option.get("optionId"))
                answer_num = option.get("answerId")
                if int(option_obj.answer_number) == int(answer_num):
                    answered_numbers += 1
            answered_percent = math.ceil(answered_numbers * 100 / questions_number)
            quiz_result = f"{quiz_obj.field.title} : {answered_percent}%"
            result_message += " , "
            result_message += quiz_result
            QuizAnswer.objects.create(user_id=request.user.id, quiz_id=quiz_obj.id, correct_percent=answered_percent)
        print(result_message)
        return JsonResponse(
            {"status": "success", "message": result_message})


class SendOtpCodeView(View):
    http_method_names = ["post"]

    def post(self, request: HttpRequest):
        phone_number = request.POST.get("phone-number")
        request.session['phone_number'] = phone_number
        duplicated_user = User.objects.filter(phone_number__exact=phone_number).exists()
        if duplicated_user:
            return JsonResponse({"status": "error", "message": "کاربری با این شماره تلفن از قبل ثبت نام کرده است"})
        return JsonResponse({"status": "success", "message": "کد تایید به شماره تلفن شما ارسال شد"})


class SubmitPhoneNumberView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'quiz_module/submit_phonenumber.html', context)

    def post(self, request):
        phone_number = request.session.get('phone_number', False)
        otp_code = request.POST.get("otp-code", False)
        request_type = request.POST.get("request-type", False)
        if not request_type:
            return JsonResponse({"status": "error", "message": "لطفا نوع درخواستتون رو مشخص کنید"})
        if phone_number and otp_code:
            if otp_code == "1234":
                if request_type == "intern":
                    redirect_url = reverse("intern_register_view")
                elif request_type == "jobseeker":
                    redirect_url = reverse("job_seeker_register_view")
                else:
                    return JsonResponse({"status": "error", "message": "لطفا نوع درخواستتون رو مشخص کنید"})
                request.session['phone_number_verified'] = True
                return JsonResponse({"status": "success", "redirect_url": redirect_url,
                                     "message": "کد تایید شما تایید شد درحال تغییر مسیر"})
            else:
                return JsonResponse({"status": "error", "message": "کد تایید اشتباه است"})
        else:
            return JsonResponse({"status": "error", "message": "شماره تلفن یا کد تایید درست وارد نشده است"})


class InternRegisterView(View):
    def get(self, request):
        intern_register_form = InternRegisterForm()
        singup_form = RegisterForm()
        context = {
            "intern_register_form": intern_register_form,
            "singup_form": singup_form,
        }
        return render(request, "quiz_module/intern_register.html", context)

    def post(self, request):
        singup_form = RegisterForm(request.POST)
        intern_register_form = InternRegisterForm(request.POST, request.FILES)
        phone_number = request.session.get('phone_number', False)
        phone_number_verified = request.session.get('phone_number_verified', False)
        if not phone_number_verified or not phone_number:
            raise Http404("لطفا ابتدا شماره تلفن خود را تایید کنید")
        if singup_form.is_valid() and intern_register_form.is_valid():
            full_name = singup_form.cleaned_data.get("full_name")
            national_code = singup_form.cleaned_data.get("national_code")
            password = singup_form.cleaned_data.get("password")
            new_user = User.objects.create_user(national_code, phone_number, password, full_name=full_name)
            # login(request, new_user)
            quiz_subscription = intern_register_form.save(commit=False)
            quiz_subscription.user = new_user
            quiz_subscription.save()
            fields_form = InternFieldForm()
            return render(request, 'quiz_module/choise_fields.html', {"fields_form": fields_form, "type": "intern"})
        else:
            context = {
                "intern_register_form": intern_register_form,
                "singup_form": singup_form,
            }
            return render(request, "quiz_module/intern_register.html", context)


class JobSeekerRegisterView(View):
    def get(self, request):
        jobseeker_register_form = JobSeekerRegisterForm()
        singup_form = RegisterForm()
        context = {
            "jobseeker_register_form": jobseeker_register_form,
            "singup_form": singup_form,
        }
        return render(request, "quiz_module/jobseeker_register.html", context)

    def post(self, request):
        singup_form = RegisterForm(request.POST)
        jobseeker_register_form = JobSeekerRegisterForm(request.POST, request.FILES)
        phone_number = request.session.get('phone_number', False)
        phone_number_verified = request.session.get('phone_number_verified', False)
        if not phone_number_verified or not phone_number:
            raise Http404("لطفا ابتدا شماره تلفن خود را تایید کنید")
        if singup_form.is_valid() and jobseeker_register_form.is_valid():
            full_name = singup_form.cleaned_data.get("full_name")
            national_code = singup_form.cleaned_data.get("national_code")
            password = singup_form.cleaned_data.get("password")
            fields_form = JobSeekerFieldForm()
            try:
                new_user = User.objects.create_user(national_code, phone_number, password, full_name=full_name)
            except Exception as e:
                return render(request, 'quiz_module/choise_fields.html',
                              {"fields_form": fields_form, "type": "jobseeker"})
            # login(request, new_user)
            quiz_subscription = jobseeker_register_form.save(commit=False)
            quiz_subscription.user = new_user
            quiz_subscription.save()

            return render(request, 'quiz_module/choise_fields.html', {"fields_form": fields_form, "type": "jobseeker"})
        else:
            context = {
                "jobseeker_register_form": jobseeker_register_form,
                "singup_form": singup_form,
            }
            return render(request, "quiz_module/jobseeker_register.html", context)


class SubmitInternFieldView(View):
    def post(self, request):
        form = InternFieldForm(request.POST)
        phone_number = request.session.get('phone_number', False)
        phone_number_verified = request.session.get('phone_number_verified', False)
        if not phone_number_verified or not phone_number:
            raise Http404("لطفا ابتدا شماره تلفن خود را تایید کنید")
        if form.is_valid():
            fields = form.cleaned_data.get("fields")
            if fields.count() > 3 or fields.count() <= 0:
                form.add_error("fields", "حداقل باید یه رشته و حداکثر سه تا رشته انتخاب کنید")
            else:
                try:
                    intern_register = InternSubscription.objects.get(user__phone_number=phone_number)
                except InternSubscription.DoesNotExist:
                    return Http404("لطفا ابتدا در آزمون ثبت نام کنید")
                for field in fields:
                    intern_register.fields.add(field)
            return render(request, 'quiz_module/quiz_success.html')
        return render(request, 'quiz_module/choise_fields.html', {"fields_form": form, "type": "intern"})


class SubmitJobSeekerFieldView(View):
    def post(self, request):
        form = JobSeekerFieldForm(request.POST)
        phone_number = request.session.get('phone_number', False)
        phone_number_verified = request.session.get('phone_number_verified', False)
        if not phone_number_verified or not phone_number:
            raise Http404("لطفا ابتدا شماره تلفن خود را تایید کنید")
        if form.is_valid():
            fields = form.cleaned_data.get("fields")
            if fields.count() > 3 or fields.count() <= 0:
                form.add_error("fields", "حداقل باید یه رشته و حداکثر سه تا رشته انتخاب کنید")
            else:
                try:
                    jobseeker_register = JobSeekerSubscription.objects.get(user__phone_number=phone_number)
                except JobSeekerSubscription.DoesNotExist:
                    return Http404("لطفا ابتدا در آزمون ثبت نام کنید")
                for field in fields:
                    jobseeker_register.fields.add(field)
            return render(request, 'quiz_module/quiz_success.html')
        return render(request, 'quiz_module/choise_fields.html', {"fields_form": form, "type": "jobseeker"})
