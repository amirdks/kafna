from django.contrib import admin

from quiz_module.models import JobSeekerField, InternField, Quiz, QuizAnswer, QuizQuestion, InternSubscription, \
    JobSeekerSubscription

# Register your models here.

admin.site.register(JobSeekerField)
admin.site.register(InternField)
admin.site.register(InternSubscription)
admin.site.register(JobSeekerSubscription)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)
