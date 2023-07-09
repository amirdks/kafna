import json
import math

from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from account_module.forms import RegisterForm
from .form_errors import form_error
from .forms import RegisterQuizForm
from .models import Quiz, QuizQuestion, QuizAnswer, InternSubscription

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
            return JsonResponse({"status": "error", "message": "شما قبلا در آزمون شرکت کرده اید برای دیدن نتیجه برروی دکمه کلیک کنید"})
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
