from django.urls import path

from account_module import views

urlpatterns = [
    path("profile/", views.UserPanelView.as_view(), name="user_panel_view"),
    path("user-panel/password-edit/", views.UserChangePasswordView.as_view(), name="user_panel_password_edit_view"),
    path("user-panel/register-detail/", views.UserPanelRegisterDetailView.as_view(),
         name="user_panel_register_detail_view"),
    path("user-panel/register-detail/edit", views.UserPanelRegisterEditView.as_view(),
         name="user_panel_register_edit_view"),
]
