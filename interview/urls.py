from django.urls import path
from . import views

app_name = 'interview'
urlpatterns = [
    path("setup", views.setup_page, name="setup_page"),
    path("interview/<int:interview_id>/question_index<int:question_index>/", views.interview_question_page,
         name="interview_question_page"),
    path("over", views.interview_over, name="over"),
    path("landingpage", views.landing_page, name="landing_page"),
    path("test/", views.test, name="test"),
    path("upload_voice/", views.upload_voice, name="upload_voice"),
]
