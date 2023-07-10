from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home_page_view"),
    path("support/", views.SupportView.as_view(), name="support_view"),
    path("about-us/", views.AboutUsView.as_view(), name="about_us_view"),
]
