from django.contrib import admin

from quiz_module.models import QuizField, Quiz

# Register your models here.

admin.site.register(QuizField)
admin.site.register(Quiz)