import re
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render
from django.db import IntegrityError
from .forms import AskQuestionForm, AnswerForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import User, Contact, Question, Answer, Comment

def index(request):
    all_questions = Question.objects.all().order_by('id').reverse()
    question_count = all_questions.count()
    questions = []
    for question in all_questions:
        tags = question.tags.split(",")
        all_answers = Answer.objects.filter(question=question)
        answers_count = all_answers.count()

        questions.append({
            'question': question,
            'tags': tags,
            'answers_count': answers_count,
        })
    return render(request, "threadfusion/index.html", {
        "all_questions": questions,
        "question_count": question_count
    })

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "threadfusion/login.html", {
                "message": "Invalid credentials"
            })
    else:
        return render(request, "threadfusion/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['cpassword']

        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$', password):
            return render(request, "threadfusion/register.html", {
                "message": "Password must contain at least 8 characters, 1 number, 1 uppercase and 1 lowercase letter."
            })

        if password != confirm_password:
            return render(request, "threadfusion/register.html", {
                "message": "Passwords are not matching"
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "threadfusion/register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "threadfusion/register.html")

def contact(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        message = request.POST['message']

        user_message = Contact(fullname=fullname, email=email, message=message)
        user_message.save()

        return render(request, "threadfusion/contact.html", {
            "alert": "Message sent successfully."
        })
    else:
        return render(request, "threadfusion/contact.html")

def askquestion(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            form.instance.user = user
            form.save()
            form = AskQuestionForm()
            return render(request, "threadfusion/askquestion.html", {
                "alert": "Question posted successfully.",
                "form": form
            })
    else:
        form = AskQuestionForm()
    return render(request, "threadfusion/askquestion.html", {'form': form})

def editquestion(request, id):
    question = Question.objects.get(pk=id)
    if request.method == 'POST':
        form = AskQuestionForm(request.POST, instance=question)
        if form.is_valid:
            form.save()
            form = AskQuestionForm()
            return render(request, "threadfusion/editquestion.html", {
                "form": form,
                "question": question,
                "alert": "Question edited successfully",
            })
    else:
        form = AskQuestionForm(instance=question)
    return render(request, "threadfusion/editquestion.html", {"form": form})

def deletequestion(request, id):
    question = Question.objects.get(pk=id)

    if request.method == 'POST':
        question_to_delete = request.POST['question-id']
        answer_to_delete = request.POST['answer-id']

        if question_to_delete and answer_to_delete:
            answer = Answer.objects.get(pk=answer_to_delete)
            answer.delete()
            return HttpResponseRedirect(reverse('singlequestion', args=[id]))
        else:
            question.delete()
            return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('index'))

def singlequestion(request, id):
    question = Question.objects.get(pk=id)
    tags = question.tags.split(",")
    all_answers = Answer.objects.filter(question=question).order_by('id').reverse()
    get_comments = Comment.objects.filter(question=question).order_by('id').reverse()
    answers_count = all_answers.count()

    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        answerForm = AnswerForm(request.POST)

        if answerForm.is_valid():
            answerForm.instance.user = user
            answerForm.instance.question = question
            answerForm.save()
            answerForm = AnswerForm()
            alert_message = "Your answer posted successfully"
        elif 'comment' in request.POST:
            answer_id = request.POST['answer_id']
            comment = request.POST['comment']
            answer = Answer.objects.get(pk=answer_id, question=question)

            new_comment = Comment(comment=comment, user=user, question=question, answer=answer)
            new_comment.save()
            alert_message = "Comment added successfully."
        else:
            alert_message = "Error! Something went wrong."
            
        return render(request, "threadfusion/singlequestion.html", {
            "question": question,
            "tags": tags,
            "all_answers": all_answers,
            "answers_count": answers_count,
            "answerForm": answerForm,
            "comments": get_comments,
            "alert": alert_message,
        })
    else:
        answerForm = AnswerForm()
    return render(request, "threadfusion/singlequestion.html", {
        "question": question,
        "tags": tags,
        "all_answers": all_answers,
        "answers_count": answers_count,
        "comments": get_comments,
        "answerForm": answerForm,
    })

def editanswer(request, question_id, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            form = AnswerForm()
            return render(request, "threadfusion/editanswer.html", {
                "form": form,
                "question_id": question_id,
                "alert": "Answer edited successfully",
            })
    else:
        form = AnswerForm(instance=answer)
    return render(request, "threadfusion/editanswer.html", {"form": form})

def tags(request, tag):
    filtered_questions = Question.objects.filter(tags__icontains=tag)
    questions = []
    for question in filtered_questions:
        tags = question.tags.split(",")
        all_answers = Answer.objects.filter(question=question)
        answers_count = all_answers.count()

        questions.append({
            'question': question,
            'tags': tags,
            'answers_count': answers_count,
        })

    return render(request, "threadfusion/tags.html", {
        "tag": tag,
        "filtered_questions": questions
    })

def search(request):
    query = request.GET.get('q', '').strip()
    questions = Question.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(tags__icontains=query)
    )
    searched_questions = []
    for question in questions:
        tags = question.tags.split(",")
        all_answers = Answer.objects.filter(question=question)
        answers_count = all_answers.count()

        searched_questions.append({
            'question': question,
            'tags': tags,
            'answers_count': answers_count,
        })
    question_count = questions.count()

    return render(request, "threadfusion/search.html", {
        "query": query,
        "question_count": question_count,
        "searched_questions": searched_questions
    })