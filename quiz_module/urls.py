from django.urls import path

from quiz_module import views

urlpatterns = [
    path("register-quiz/", views.RegisterQuizView.as_view(), name="register_quiz_view"),
    path("test/", views.Test.as_view(), name="test"),
]
