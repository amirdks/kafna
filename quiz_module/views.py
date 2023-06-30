from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .forms import RegisterQuizForm


# Create your views here.
class RegisterQuizView(View):
    def get(self, request):
        form = RegisterQuizForm()
        context = {
            'form': form
        }
        return render(request, "quiz_module/register_quiz_page.html", context)

    def post(self, request):
        form = RegisterQuizForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "quiz_module/quiz_success.html")
        context = {
            'form': form
        }
        return render(request, "quiz_module/register_quiz_page.html", context)


class Test(TemplateView):
    template_name = "quiz_module/quiz_success.html"
