from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .form_errors import form_error
from .forms import RegisterQuizForm


# Create your views here.
class RegisterQuizView(View):
    def get(self, request):
        form = RegisterQuizForm()
        register_form = RegisterForm()
        context = {
            'form': form,
            'register_form':register_form,
        }
        return render(request, "quiz_module/register_quiz_page.html", context)

    def post(self, request):
        form = RegisterQuizForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "quiz_module/quiz_success.html")
        error = form_error(form)
        context = {
            'form': form
        }
        return render(request, "quiz_module/register_quiz_page.html", context)


