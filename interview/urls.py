from django.urls import path
from . import views

app_name = 'interview'
urlpatterns = [
    path("setup", views.setup_page, name="setup_page"),
    path("interview/<int:interview_id>/question_index<int:question_index>/", views.interview_question_page,
         name="interview_question_page"),
    path("summary", views.interview_summary, name="summary"),
    path("landingpage", views.landing_page, name="landing_page"),
    path("test/", views.test, name="test"),
    path("upload_voice/", views.upload_voice, name="upload_voice"),

    path("career_background", views.career_background, name="career_background"),
    path("career_interests", views.career_interests, name="career_interests"),
    path("career_intro", views.career_intro, name="career_intro"),
    path("career_preferences", views.career_preferences, name="career_preferences"),
    path("career_results", views.career_results, name="career_results"),
    path("career_chat", views.career_chat, name="career_chat"),
    path("career_personality", views.career_personality, name="career_personality"),
    path("track_intro", views.track_intro, name="track_intro"),

    path('register', views.user_register, name='register'),
    path('login', views.user_login, name='login'),

]
