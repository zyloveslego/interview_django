from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect, HttpResponse
from .models import InterviewInfo, User, Question, InterviewQuestion

import random

from django.views.decorators.csrf import csrf_exempt

import whisper

from django.http import JsonResponse

import openai


# Create your views here.

# interview set up page
def setup_page(request):
    if request.method == 'POST':
        # Process the form data
        print(request.POST.keys())
        question = request.POST['n_question']
        year = request.POST['YOE']
        role = request.POST['role']

        print("Question: " + str(question))
        print("Year: " + str(year))
        print("Role: " + str(role))

        # save to the database
        print("write into database; generate interview ID")
        # print(role)
        # print(year)
        # print(question)

        # temp generate user
        user_instance = User.objects.filter(user_id=1)[0]
        # print(user_instance)

        # generate interview
        setup_info = InterviewInfo(
            used_id=user_instance,
            total_question=int(question),
            year_of_experience=int(year),
            role="IC",
            total_time=0)
        setup_info.save()

        # generate interview questions
        random_list = random.sample(range(1, Question.objects.count()), int(question))
        print(random_list)
        for index, random_n in enumerate(random_list):
            question_interview = InterviewQuestion(
                interview_id=setup_info,
                question_id=Question.objects.filter(question_id=random_n)[0],
                question_index=index + 1,
            )
            question_interview.save()

        # Redirect to interview page
        return redirect('interview:interview_question_page',
                        interview_id=str(setup_info.interview_id),
                        question_index=1)
    else:
        # If it's not a POST request, just render the form
        return render(request, 'interview/setup_page.html')


# interview question page
def interview_question_page(request, interview_id, question_index):
    interview_info = InterviewInfo.objects.filter(interview_id=interview_id)[0]
    interview_question = InterviewQuestion.objects.filter(interview_id=interview_id, question_index=question_index)
    if interview_question.exists():
        interview_question = interview_question[0]
        question = Question.objects.filter(question_id=int(interview_question.question_id.question_id))[0]

        form = {"role": "IC",
                "year_of_experience": interview_info.year_of_experience,
                "length_of_interview": interview_info.total_question,
                "current_question": question_index,
                "question_text": question.question_text,
                }
        return render(request, 'interview/interview_question_page.html', {"form": form})
    else:
        return redirect('interview:summary')


# interview over
def interview_summary(request):
    return render(request, 'interview/interviewsummary.html')


# landing page
def landing_page(request):
    return render(request, 'interview/landingpage.html')


# save voice file
def save_uploaded_file(file: InMemoryUploadedFile, file_path: str) -> None:
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    file.close()


# get response from chatgpt
def get_access_from_chatgpt(question_text, answer_text):
    prompt_from_file = open("./interview/interview_data/access_prompt.txt")
    prompt_default = prompt_from_file.read()
    prompt = (prompt_default + "\n\n" + "Interviewer Question: " + question_text + "\n" + "Interviewee Answer: " +
              answer_text)
    print(prompt)

    openai.api_key = "C"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    # print(response)
    my_content = response['choices'][0]['message']['content']
    # print(my_content)

    return my_content


# receive upload voice
@csrf_exempt
def upload_voice(request):
    if request.method == 'POST':
        voice_file = request.FILES.get('audio_data')
        if voice_file:
            # Process the voice file here, e.g. save it to a database or process it with a speech recognition library.
            print(voice_file)
            save_uploaded_file(voice_file, "./recorded_voice/" + str(voice_file))
            # voice to text
            # options = whisper.DecodingOptions(language='en', fp16=False)
            model = whisper.load_model("tiny")
            result = model.transcribe("./recorded_voice/" + str(voice_file), fp16=False, language='English')

            print(result["text"].strip())
            print(request.POST['question_text'])

            voice_text = result["text"].strip()
            question_text = request.POST['question_text']

            my_access = get_access_from_chatgpt(question_text, voice_text)

            print(my_access)

            return JsonResponse({'success': True, "voice_text": voice_text, "my_access": my_access})
        else:
            return JsonResponse({'success': False, 'error': 'No voice file was uploaded.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})


# test
def test(request):
    return render(request, 'interview/anchor_test.html')


# career part
def career_background(request):
    return render(request, 'interview/career-builder-background.html')


def career_interests(request):
    return render(request, 'interview/career-builder-interests.html')


def career_intro(request):
    return render(request, 'interview/career-builder-intro.html')


def career_preferences(request):
    return render(request, 'interview/career-builder-preferences.html')


def career_results(request):
    return render(request, 'interview/career-builder-results.html')
