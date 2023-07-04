from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from quiz_module.models import QuizAnswer


# Create your views here.
class UserPanelView(LoginRequiredMixin, View):
    def get(self, request):
        answers = QuizAnswer.objects.filter(user_id=request.user.id)
        context = {
            "answers": answers,
        }
        return render(request, 'account_module/user_panel.html', context)
