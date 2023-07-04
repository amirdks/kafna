from django.urls import path

from account_module import views

urlpatterns = [
    path("user-panel/", views.UserPanelView.as_view(), name="user_panel_view")
]
