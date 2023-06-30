from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


# Create your views here.
class IndexView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'main_module/home_page.html', context)
