import torch.cuda
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect, HttpResponse
from .models import InterviewInfo, Question, InterviewQuestion
from django.contrib.auth.models import User
from .forms import NewUserForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import random
from django.views.decorators.csrf import csrf_exempt
import whisper
from django.http import JsonResponse, HttpResponseNotFound
import openai
from decouple import config
import re
from django.core import serializers
from interview_django_v2 import settings

# model = whisper.load_model("tiny")
openai.api_key = ""


# Create your views here.

# interview set up page
@login_required()
def setup_page(request):
    if request.method == 'POST':
        # Process the form data
        # print(request.POST.keys())
        # print(request.user.username)
        question = request.POST['n_question']
        year = request.POST['YOE']
        role = request.POST['role']

        current_user = request.user.username

        # print("Question: " + str(question))
        # print("Year: " + str(year))
        # print("Role: " + str(role))

        # TODO: save to database
        # save to database
        print("write into database; generate interview ID")

        # temp generate user
        user_instance = User.objects.filter(username=str(current_user))[0]
        # print(user_instance)

        # generate interview
        setup_info = InterviewInfo(
            user_id=user_instance,
            total_question=int(question),
            year_of_experience=int(year),
            role="IC",
            total_time=0)
        setup_info.save()

        # generate interview questions
        random_list = random.sample(range(1, Question.objects.count()), int(question))
        print(random_list)

        # temp Q2, Q4, Q10
        temp_list = [2, 4, 17]
        random_list = temp_list + random_list
        random_list = random_list[0:int(question)]
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
@login_required()
def interview_question_page(request, interview_id, question_index):
    interview_info = InterviewInfo.objects.filter(interview_id=interview_id)[0]
    # print(interview_info.user_id)
    # print(request.user.username)
    # print(type(request.user.username))
    # print(type(interview_info.user_id))
    if str(request.user.username) != str(interview_info.user_id):
        return HttpResponseNotFound("<h1>Page not found</h1>")
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
# TODO: user check
@login_required()
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
    destination.close()


# get response from chatgpt
def get_answer_from_chatgpt(question_text, answer_text):
    access_prompt_from_file = open("./interview/interview_data/access_prompt.txt")
    access_prompt_default = access_prompt_from_file.read()
    access_prompt = access_prompt_default + "\n\n" + "Interviewer Question: " + "\"" + question_text + "\"" + "\n" + "Interviewee Answer: " + "\"" + answer_text + "\""
    access_prompt_from_file.close()

    print("access_prompt")
    print(access_prompt)
    print("access_prompt end")

    rewrite_prompt_from_file = open("./interview/interview_data/rewrite_prompt.txt")
    rewrite_prompt_default = rewrite_prompt_from_file.read()
    rewrite_prompt = rewrite_prompt_default
    rewrite_prompt_from_file.close()
    # print(rewrite_prompt)

    print("getting access")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": access_prompt},
        ],
        temperature=0.2,
    )

    access_answer_content = response['choices'][0]['message']['content']
    print("-------------")
    print(access_answer_content)
    print("-------------")

    print("getting rewrite")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": access_prompt},
            {"role": "assistant", "content": access_answer_content},
            {"role": "user", "content": rewrite_prompt},
        ]
    )

    rewrite_answer_content = response['choices'][0]['message']['content']
    print("-------------")
    print(rewrite_answer_content)

    return access_answer_content, rewrite_answer_content


def format_access(text):
    try:
        # Split the text into lines
        lines = text.split('\n')
        lines = [line for line in lines if line != '']
        print(lines)

        # Regular expression pattern to extract the word and score
        pattern = r'\d+\.\s.*?(\d/10)'

        format_text = ""

        # Iterate through each line and extract the word and score
        for line in lines[0:-1]:
            match = re.search(pattern, line)
            item_text = match.group(0)
            start_index = match.start()
            end_index = match.end()

            # print(f"Start Index: {start_index}, End Index: {end_index}")
            # print(item_text)

            insert_text = "<span>"
            part1 = line[:start_index]
            part2 = line[start_index:]
            line = part1 + insert_text + part2

            insert_text = "</span>"
            part1 = line[:(end_index + 6)]
            part2 = line[(end_index + 6):]
            line = part1 + insert_text + part2

            insert_text = "<br><br>"
            line = line + insert_text

            # print(line)

            format_text = format_text + line

        word_to_find = "Overall"
        start_index = lines[-1].find(word_to_find)
        end_index = start_index + len(word_to_find)

        insert_text = "<span>"
        part1 = lines[-1][:start_index]
        part2 = lines[-1][start_index:]
        lines[-1] = part1 + insert_text + part2

        insert_text = "</span>"
        part1 = lines[-1][:(end_index + 6)]
        part2 = lines[-1][(end_index + 6):]
        lines[-1] = part1 + insert_text + part2

        format_text = format_text + "<br><br>" + lines[-1]

    except BaseException as e:
        print(e)
        return text

    return format_text


def format_rewrite(text):
    # Find the index of the first and last double quotes
    first_quote_index = text.find('"')
    last_quote_index = text.rfind('"')

    # Extract the text between the first and last double quotes
    result = text[first_quote_index + 1:last_quote_index]

    return result


# TODO: 音频文件怎么处理、gpt使用次数限制
# receive upload voice and ask gpt
@csrf_exempt
@login_required()
def upload_voice(request):
    if request.method == 'POST':
        voice_file = request.FILES.get('audio_data')
        if voice_file:
            # Process the voice file here, e.g. save it to a database or process it with a speech recognition library.
            print(voice_file)
            save_uploaded_file(voice_file, "./recorded_voice/" + str(voice_file) + ".mp3")

            file = open("./recorded_voice/" + str(voice_file) + ".mp3", "rb")
            transcription = openai.Audio.transcribe("whisper-1", file)
            voice_text = transcription.get("text")

            # # voice to text
            # # options = whisper.DecodingOptions(language='en', fp16=False)
            # model = whisper.load_model("tiny")
            # result = model.transcribe("./recorded_voice/" + str(voice_file), fp16=False, language='English')
            # # result = model.transcribe(voice_file, fp16=False, language='English')
            #
            # print(result["text"].strip())
            # print(request.POST['question_text'])
            #
            # voice_text = result["text"].strip()
            question_text = request.POST['question_text']

            # model.cpu()
            # del model
            # torch.cuda.empty_cache()

            access_answer_content, rewrite_answer_content = get_answer_from_chatgpt(question_text, voice_text)
            # access_answer_content, rewrite_answer_content = 123, 123

            question_index = int(request.POST['question_index'])
            interview_id = InterviewInfo.objects.get(interview_id=int(request.POST['interview_id']))

            current_iq = InterviewQuestion.objects.get(interview_id=interview_id, question_index=question_index)
            current_iq.user_answer = voice_text
            current_iq.access_answer = access_answer_content
            current_iq.revise_answer = rewrite_answer_content
            current_iq.save()

            return JsonResponse(
                {'success': True,
                 "voice_text": voice_text,
                 "my_access": format_access(access_answer_content),
                 "my_revise": format_rewrite(rewrite_answer_content)
                 })

            # TODO: error类型需要更新
        else:
            return JsonResponse({'success': False, 'error': 'No voice file was uploaded.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})


# dashboard页面
def dashboard(request):
    pass
    return render(request, 'interview/dashboard.html')


# 显示已答题和未答题
# 这里面可能存在一个问题，一道题可能回答过多次
def question_list(request):
    pass


# 显示所有interview
@csrf_exempt
def interview_list(request):
    interview_data = InterviewInfo.objects.all()
    pk_name = InterviewInfo._meta.pk.name
    pk_values = [getattr(obj, pk_name) for obj in interview_data]
    interview_data = serializers.serialize('json', interview_data)
    return JsonResponse({'success': True, "interview_data": interview_data, "pk_values": pk_values})


# 显示单次interview的所有question
def questions_list_in_interview(request, interview_id):
    print(interview_id)
    interview_questions = InterviewQuestion.objects.filter(interview_id=interview_id)
    # interview_questions_data = serializers.serialize('json', interview_questions)
    # print(interview_questions_data)
    return render(request, 'interview/interview_questions.html', {'interview_questions': interview_questions})


# temp use, delete later
# @csrf_exempt
# @login_required()
# def upload_voice(request):
#     if request.method == 'POST':
#         voice_file = request.FILES.get('audio_data')
#         if voice_file:
#
#             question_index = request.POST['question_index']
#
#             import time
#             time.sleep(2)
#
#             if question_index == "1":
#                 print(1)
#                 voice_text = "There was one time when I had a disagreement with a coworker over how to approach a certain project we were collaborating on. I don't remember all the details now, but we had different opinions on the best method to use. I think both of us felt pretty strongly that our own approach was the right one. Looking back, I wish I had made more of an effort to see their perspective and find common ground.<br><br>At the time, I think I just tried to argue for my viewpoint without really listening to their reasoning. The conflict started to escalate and get a bit heated until our manager stepped in. They had us explain our diverging approaches and suggested a compromise that seemed to work okay for both of us. In the end, we got the project done but I don't think either of us was very happy with how it turned out.<br><br>In hindsight, I should have handled the disagreement in a more constructive, level-headed way from the start. I could have made more of an effort to understand their viewpoint and tried to find a solution we both felt good about."
#                 my_access = "<span>1. Relevance: 5/10</span> - The candidate's answer addresses the conflict with a coworker, which is relevant to the interviewer's question. However, it lacks specific details about the conflict and the skills the interviewer may be looking for.<br><br><span>2. Specificity: 4/10</span> - The answer is quite vague as it lacks specific details about the project, the nature of the disagreement, and the actions taken. More specific information would provide better context.<br><br><span>3. Actions: 4/10</span> - While the candidate mentions they argued for their viewpoint and didn't listen to their coworker, they don't elaborate on the specific actions they took to resolve the conflict. There's a lack of concrete steps or strategies employed.<br><br><span>4. Results and Impact: 3/10</span> - The answer does not provide information about the outcome or impact of the conflict resolution. It's unclear whether the project was successful or not, and if any lessons were learned from this experience.<br><br><span>5. Learning: 6/10</span> - The candidate acknowledges that they should have handled the disagreement differently in hindsight, showing a willingness to learn from their past behavior. However, they don't delve into specific lessons learned or how they would improve in a similar situation.<br><br><span>6. Clarity: 7/10</span> - The answer is generally clear and easy to follow, but it lacks depth and specific examples that would make it more compelling.<br><br><span>7. Soft skills: 5/10</span> - The answer touches on some soft skills like communication (albeit negatively), but it doesn't showcase a wide range of skills like problem-solving or conflict resolution.<br><br><span>Overall</span> - I would rate the answer a 5/10. The response is somewhat relevant to the question, but it lacks specificity, actionable steps, and a clear indication of the impact of the candidate's actions. It does show a willingness to learn but could benefit from more concrete examples and outcomes to make it more effective."
#                 my_revise = "Of course, I can provide a more detailed example of a conflict with a coworker. In a previous role, I was collaborating with a colleague on a critical project that had tight deadlines. We had different approaches to solving a key problem, and tensions were rising.<br><br>To address this conflict, I took several steps. First, I initiated a one-on-one meeting with my coworker to openly discuss our differing viewpoints. I actively listened to their perspective without interrupting and asked clarifying questions to ensure I understood their reasoning. This helped create a more empathetic and collaborative atmosphere.<br><br>Next, we decided to involve our manager to mediate the discussion. During this meeting, I presented my ideas clearly and professionally, highlighting the potential benefits of my approach. However, I also acknowledged the strengths in my coworker's approach and how it aligned with certain project requirements.<br><br>Our manager facilitated a productive conversation that led to a compromise. We agreed to combine elements of both our approaches, which ultimately improved the project's outcome. By doing so, we not only met our deadlines but also enhanced the quality of our work.<br><br>Reflecting on this experience, I recognized the importance of effective communication and compromise in resolving conflicts. It reinforced my belief in the power of collaboration and taught me the value of seeking common ground when working with diverse viewpoints. I've since applied these lessons to subsequent collaborations, resulting in smoother teamwork and more successful outcomes."
#             elif question_index == "2":
#                 print(2)
#                 voice_text = "Looking back on my career so far, one workplace situation I often reflect on is when I had a miscommunication with a colleague that led to some tension between us. This colleague and I were both working on the same client account, but I made the mistaken assumption that they would take the lead on an important presentation we had coming up. Without checking in with them explicitly, I put all my focus into other aspects of the project, thinking they had the presentation covered. However, as we got closer to the due date, it became clear there had been a misunderstanding - they had thought I was preparing the presentation deck. We both felt frustrated and probably said some blunt things out of stress in the moment. I wish I had proactively communicated earlier and confirmed roles and expectations before making assumptions. If I could do it over again, I would have approached them early on and said \"Just wanted to check - are you planning to take the lead on the client presentation? Or should I plan to tackle it?\""
#                 my_access = "<span>1. Relevance: 8/10</span> - The candidate's answer is relevant to the question, as it discusses a specific mistake and a situation with a colleague, which is what the interviewer asked for.<br><br><span>2. Specificity: 7/10</span> - The answer provides a reasonably specific example with some context, such as the miscommunication about the client presentation. However, it could benefit from more details about the project, the nature of the tension, and the specific consequences of the miscommunication.<br><br><span>3. Actions: 7/10</span> - The candidate articulates the actions they would take if they could do it over again, which is helpful. However, the answer lacks a clear description of the actions they took at the time of the mistake. It would be more impactful if they described the steps they actually took to address the situation initially.<br><br><span>4. Results and Impact: 6/10</span> - While the answer acknowledges that there was frustration and stress, it doesn't provide a clear picture of the ultimate impact of the mistake. Did the presentation suffer as a result of the miscommunication? Were there any long-term consequences? More information about the results and impact would improve this aspect.<br><br><span>5. Learning: 8/10</span> - The candidate mentions that they wish they had communicated proactively and confirmed roles and expectations. This shows a willingness to learn from the mistake and improve in the future, demonstrating a growth mindset.<br><br><span>6. Clarity: 8/10</span> - The answer is relatively clear and concise. It's easy to follow the narrative of the situation and the candidate's reflection on it.<br><br><span>7. Soft skills: 7/10</span> - The answer touches on soft skills like communication and teamwork, as the candidate acknowledges the importance of proactive communication and avoiding assumptions. However, it doesn't delve deeply into these skills or provide concrete examples of how they were applied.<br><br><span>Overall</span> - I would rate the answer a 7/10. The response is relevant and shows a willingness to learn from mistakes, but it could benefit from more specific details about the situation, actions taken, and the impact of the mistake. Additionally, a deeper exploration of soft skills would enhance the answer's quality."
#                 my_revise = "Absolutely, reflecting on my career, there's a particular incident that stands out where I believe I could have handled a situation with a colleague more effectively. This happened during a crucial project where my colleague and I were both responsible for a client presentation. Unfortunately, I made the assumption that my colleague would take the lead on creating the presentation while I concentrated on other aspects of the project. <br><br>As the deadline approached, it became painfully evident that we had miscommunicated. My colleague had assumed I was in charge of the presentation deck, and neither of us had confirmed these roles explicitly. The tension between us increased as the pressure mounted, and regrettably, we exchanged some sharp words in the heat of the moment.<br><br>In hindsight, I recognize that I should have taken proactive steps to prevent this situation. Instead of making assumptions, I should have initiated clear and open communication with my colleague from the beginning. I could have approached them early on and said something like, 'Let's clarify our roles for the client presentation. Are you planning to take the lead on it, or should I plan to tackle it?'<br><br>The result of this miscommunication was not only tension but also a less-than-ideal client presentation. The impact was clear: it affected our professionalism and potentially our client's perception. <br><br>From this experience, I've learned the critical importance of proactive communication and role clarification in teamwork. I now make it a point to ensure everyone's roles and expectations are crystal clear right from the start of any project. It's a lesson that has helped me improve my collaboration and prevent similar situations from arising in the future."
#             elif question_index == "3":
#                 print(3)
#                 voice_text = "Looking back on my career so far, one situation where I failed stands out. I was leading a team project that was meant to develop a new marketing campaign for one of our major clients. I didn't properly scope the project initially and made some wrong assumptions about what could be accomplished in the given timeline. As a result, when the deadline arrived, we were behind where we needed to be. I reacted by trying to push the team to work longer hours to catch up.In hindsight, that was the wrong approach. I put too much pressure on the team and didn't listen to their feedback that the timeline was unrealistic. When we ultimately missed the final deadline, I took responsibility for the failure when speaking to my manager. From that experience, I learned the importance of thoroughly planning projects, having open lines of communication with teams, and listening to feedback. Instead of just driving harder to meet the unrealistic deadline, I should have worked with my manager and the client to properly re-scope the project. Although we missed the initial deadline, we were able to refocus our efforts and ultimately deliver a successful campaign for the client."
#                 my_access = "<span>1. Relevance: 9/10</span> - The candidate's answer directly addresses the question about a time they failed and how they dealt with it. It's highly relevant to the interviewer's query.<br><br><span>2. Specificity: 8/10</span> - The answer provides a specific example of a project involving a marketing campaign and a missed deadline. However, it could benefit from more specific details about the project or the consequences of missing the initial deadline.<br><br><span>3. Actions: 8/10</span> - The candidate outlines their actions, such as pushing the team to work longer hours and taking responsibility for the failure. However, it would be more beneficial if they described specific steps they took to rectify the situation beyond just taking responsibility.<br><br><span>4. Results and Impact: 7/10</span> - The candidate mentions that they ultimately delivered a successful campaign, but they don't provide concrete details about the positive results or the quantifiable impact of their actions.<br><br><span>5. Learning: 9/10</span> - The candidate demonstrates a clear understanding of what they learned from the situation, including the importance of project planning, open communication, and listening to feedback. This highlights a growth mindset.<br><br><span>6. Clarity: 9/10</span> - The answer is clear and easy to follow, with a logical structure.<br><br><span>7. Soft skills: 8/10</span> - The answer illustrates soft skills such as leadership, communication, and the ability to reflect on and learn from mistakes.<br><br><span>Overall</span> - I would rate the answer an 8/10. The interviewee provides a relevant and clear response to the question, showing self-awareness and a willingness to learn from their failures. However, more specific details about the project and its outcomes would have strengthened the answer and highlighted their impact more effectively."
#                 my_revise = "Absolutely, I'd be happy to share a specific experience where I faced a significant challenge and how I handled it.<br><br>In a previous role, I was leading a crucial team project focused on developing a new marketing campaign for one of our major clients. Initially, I made the mistake of not conducting a thorough project scoping, which led to incorrect assumptions about what could realistically be accomplished within the given timeline. As we neared the deadline, it became evident that we were falling behind schedule.<br><br>In response, I regrettably tried to solve the issue by pushing the team to work longer hours to catch up. Looking back, I realize that this approach was misguided and put undue pressure on the team. I failed to heed their valuable feedback that the timeline was unrealistic.<br><br>As the final deadline approached, and it became apparent that we couldn't meet it, I knew it was time to take responsibility for the failure. I had an open and honest conversation with my manager, explaining the challenges we faced and the reasons for the project's delay.<br><br>From this experience, I learned some invaluable lessons. First and foremost, I now understand the critical importance of meticulously planning projects from the outset, ensuring that all stakeholders have a realistic understanding of what can be achieved within a given timeframe. Additionally, I learned the significance of fostering open lines of communication with the team and genuinely listening to their insights and concerns. Rather than solely driving harder to meet an unrealistic deadline, I now understand the importance of collaborating with my manager and the client to appropriately adjust the project scope.<br><br>Although we missed the initial deadline, this setback allowed us to refocus our efforts and ultimately deliver a highly successful marketing campaign for the client. This experience reinforced my commitment to continuous improvement and the importance of adapting to challenges in a more constructive manner."
#             else:
#                 print(0)
#                 voice_text = "Looking back on my career so far, one situation where I failed stands out. I was leading a team project that was meant to develop a new marketing campaign for one of our major clients. I didn't properly scope the project initially and made some wrong assumptions about what could be accomplished in the given timeline. As a result, when the deadline arrived, we were behind where we needed to be. I reacted by trying to push the team to work longer hours to catch up.In hindsight, that was the wrong approach. I put too much pressure on the team and didn't listen to their feedback that the timeline was unrealistic. When we ultimately missed the final deadline, I took responsibility for the failure when speaking to my manager. From that experience, I learned the importance of thoroughly planning projects, having open lines of communication with teams, and listening to feedback. Instead of just driving harder to meet the unrealistic deadline, I should have worked with my manager and the client to properly re-scope the project. Although we missed the initial deadline, we were able to refocus our efforts and ultimately deliver a successful campaign for the client."
#                 my_access = "<span>1. Relevance: 9/10</span> - The candidate's answer directly addresses the question about a time they failed and how they dealt with it. It's highly relevant to the interviewer's query.<br><br><span>2. Specificity: 8/10</span> - The answer provides a specific example of a project involving a marketing campaign and a missed deadline. However, it could benefit from more specific details about the project or the consequences of missing the initial deadline.<br><br><span>3. Actions: 8/10</span> - The candidate outlines their actions, such as pushing the team to work longer hours and taking responsibility for the failure. However, it would be more beneficial if they described specific steps they took to rectify the situation beyond just taking responsibility.<br><br><span>4. Results and Impact: 7/10</span> - The candidate mentions that they ultimately delivered a successful campaign, but they don't provide concrete details about the positive results or the quantifiable impact of their actions.<br><br><span>5. Learning: 9/10</span> - The candidate demonstrates a clear understanding of what they learned from the situation, including the importance of project planning, open communication, and listening to feedback. This highlights a growth mindset.<br><br><span>6. Clarity: 9/10</span> - The answer is clear and easy to follow, with a logical structure.<br><br><span>7. Soft skills: 8/10</span> - The answer illustrates soft skills such as leadership, communication, and the ability to reflect on and learn from mistakes.<br><br><span>Overall</span> - I would rate the answer an 8/10. The interviewee provides a relevant and clear response to the question, showing self-awareness and a willingness to learn from their failures. However, more specific details about the project and its outcomes would have strengthened the answer and highlighted their impact more effectively."
#                 my_revise = "Absolutely, I'd be happy to share a specific experience where I faced a significant challenge and how I handled it.<br><br>In a previous role, I was leading a crucial team project focused on developing a new marketing campaign for one of our major clients. Initially, I made the mistake of not conducting a thorough project scoping, which led to incorrect assumptions about what could realistically be accomplished within the given timeline. As we neared the deadline, it became evident that we were falling behind schedule.<br><br>In response, I regrettably tried to solve the issue by pushing the team to work longer hours to catch up. Looking back, I realize that this approach was misguided and put undue pressure on the team. I failed to heed their valuable feedback that the timeline was unrealistic.<br><br>As the final deadline approached, and it became apparent that we couldn't meet it, I knew it was time to take responsibility for the failure. I had an open and honest conversation with my manager, explaining the challenges we faced and the reasons for the project's delay.<br><br>From this experience, I learned some invaluable lessons. First and foremost, I now understand the critical importance of meticulously planning projects from the outset, ensuring that all stakeholders have a realistic understanding of what can be achieved within a given timeframe. Additionally, I learned the significance of fostering open lines of communication with the team and genuinely listening to their insights and concerns. Rather than solely driving harder to meet an unrealistic deadline, I now understand the importance of collaborating with my manager and the client to appropriately adjust the project scope.<br><br>Although we missed the initial deadline, this setback allowed us to refocus our efforts and ultimately deliver a highly successful marketing campaign for the client. This experience reinforced my commitment to continuous improvement and the importance of adapting to challenges in a more constructive manner."
#
#             return JsonResponse(
#                 {'success': True, "voice_text": voice_text, "my_access": my_access, "my_revise": my_revise})
#         else:
#             return JsonResponse({'success': False, 'error': 'No voice file was uploaded.'})
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method.'})


# test
def test(request):
    # import pandas as pd
    # questions_from_file = pd.read_csv("./interview/interview_data/behaviorQuestions.csv", sep=',')
    # df = pd.DataFrame(questions_from_file)
    #
    # for i in range(len(df)):
    #     row = df[i:i + 1]
    #     # print(row['Question'][i], '\n')
    #     question = Question(
    #         question_type='IC',
    #         question_text=row['Question'][i],
    #     )
    #     question.save()

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


def career_chat(request):
    return render(request, 'interview/career-builder-chat.html')


def career_personality(request):
    return render(request, 'interview/career-builder-personality.html')


def track_intro(request):
    return render(request, 'interview/track_intro.html')


# register
def user_register(request):
    if request.method == "POST":
        form = NewUserForm(data=request.POST)
        # TODO: try return field error
        # for field in form:
        #     print("Field Error:", field.name, field.errors)

        if form.is_valid() and form.cleaned_data['access_code'] == "newship666":
            user = form.save()
            login(request, user)
            # messages.success(request, "Registration successful.")
            return redirect("interview:login")

        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()
    return render(request, 'interview/register.html', context={"register_form": form})


# login
def user_login(request):
    # if logged in, jump to landing page
    if request.user.username is not None and request.user.username != "":
        return redirect('interview:landing_page')

    # log in
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                return redirect("interview:landing_page")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = CustomAuthenticationForm()

    return render(request, 'interview/login.html', context={"login_form": form})


# log out test use
def user_logout(request):
    logout(request)
    return redirect('interview:landing_page')
