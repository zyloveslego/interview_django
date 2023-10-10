from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import User


# Create your models here.

# interview question
class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    QUESTION_TYPE_CHOICE = (
        ('IC', 'IC'),
        ('Manager', 'Manager'),
    )
    question_type = models.CharField(
        choices=QUESTION_TYPE_CHOICE,
        default='IC',
        max_length=20,
    )
    question_text = models.CharField(max_length=200)


# User
# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     # mail
#     # name
#     pass


# interview info table
class InterviewInfo(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default="test")
    interview_id = models.AutoField(primary_key=True)
    total_question = models.IntegerField(default=1)
    year_of_experience = models.IntegerField(default=0)
    ROLE_CHOICE = [
        ('IC', 'IC'),
        ('Manager', 'Manager'),
    ]
    role = models.CharField(choices=ROLE_CHOICE, max_length=20)
    total_time = models.IntegerField(default=0)  # unit second


# interview question
class InterviewQuestion(models.Model):
    interview_id = models.ForeignKey(InterviewInfo, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_index = models.IntegerField(default=1)
    user_answer = models.CharField(max_length=2000)
    access_answer = models.CharField(max_length=2000)
    revise_answer = models.CharField(max_length=2000)
