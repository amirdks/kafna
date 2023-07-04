from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from quiz_module.models import QuizAnswer


# Create your views here.
class IndexView(View):
    def get(self, request):
        answers = None
        if request.user.is_authenticated:
            answers = QuizAnswer.objects.filter(user_id=request.user.id)
        context = {
            "answers": answers,
        }
        return render(request, 'main_module/home_page.html', context)
