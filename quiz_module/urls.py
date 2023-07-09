from django.urls import path

from quiz_module import views

urlpatterns = [
    path("jobseeker-register/", views.JobSeekerRegisterView.as_view(), name="job_seeker_register_view"),
    path("intern-register/", views.InternRegisterView.as_view(), name="intern_register_view"),
    path("send-otp/", views.SendOtpCodeView.as_view(), name="send_otp_code_view"),
    path("submit-phone-number/", views.SubmitPhoneNumberView.as_view(), name="submit_phone_number_view"),
    path("submit-intern-fields/", views.SubmitInternFieldView.as_view(), name="submit_inter_fields_view"),
    path("submit-jobseeker-fields/", views.SubmitJobSeekerFieldView.as_view(), name="submit_job_seeker_fields_view"),
    path("test/", views.TestView.as_view(), name="test_view"),
    path("quiz/", views.QuizView.as_view(), name="quiz_view")
]
