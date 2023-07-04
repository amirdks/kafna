from django.contrib import admin

from quiz_module.models import QuizField, QuizSubscription, Quiz, QuizAnswer, QuizQuestion

# Register your models here.

admin.site.register(QuizField)
admin.site.register(QuizSubscription)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)
