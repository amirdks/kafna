from django.contrib import admin

from quiz_module.models import QuizField, Quiz, QuizAnswer, QuizQuestion, InternSubscription

# Register your models here.

admin.site.register(QuizField)
admin.site.register(InternSubscription)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)
