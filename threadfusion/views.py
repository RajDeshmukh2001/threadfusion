import re
import json
from django.db.models import Q
from django.urls import reverse
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from .forms import AskQuestionForm, AnswerForm, ProfileForm
from django.contrib.auth import authenticate, login, logout

from .models import User, Question, Answer, Comment, Profile, Follow, Like, Contact

def index(request):
    all_questions = Question.objects.all().order_by('id').reverse()

    paginator = Paginator(all_questions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    questions = []
    for question in page_obj:
        tags = [t.strip() for t in question.tags.split(",")]
        all_answers = Answer.objects.filter(question=question)
        answers_count = all_answers.count()

        questions.append({
            'question': question,
            'tags': tags,
            'answers_count': answers_count,
        })
    return render(request, "threadfusion/index.html", {
        "all_questions": all_questions,
        "questions": questions,
        "page_obj": page_obj,
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

        if len(username) < 3:
            return render(request, "threadfusion/register.html", {
                "message": "Username must be at least 3 characters long"
            })

        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{6,}$', password):
            return render(request, "threadfusion/register.html", {
                "message": "Password must contain at least 6 characters, 1 number, 1 uppercase and 1 lowercase letter."
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
    tags = [t.strip() for t in question.tags.split(",")]
    all_answers = Answer.objects.filter(question=question).order_by('id').reverse()
    get_comments = Comment.objects.filter(question=question).order_by('id').reverse()
    answers_count = all_answers.count()

    success_message = None
    error_message = None

    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        answerForm = AnswerForm(request.POST)

        if answerForm.is_valid():
            answerForm.instance.user = user
            answerForm.instance.question = question
            answerForm.save()
            answerForm = AnswerForm()
            success_message = "Your answer posted successfully"
        elif 'comment' in request.POST:
            answer_id = request.POST['answer_id']
            comment = request.POST['comment']

            if comment.strip() == "":
                error_message = "Comment cannot be empty."
            else:
                answer = Answer.objects.get(pk=answer_id, question=question)
                new_comment = Comment(comment=comment, user=user, question=question, answer=answer)
                new_comment.save()
                success_message = "Comment added successfully."
        else:
            error_message = "Field cannot be empty"
            
        return render(request, "threadfusion/singlequestion.html", {
            "question": question,
            "tags": tags,
            "all_answers": all_answers,
            "answers_count": answers_count,
            "answerForm": answerForm,
            "comments": get_comments,
            "success_message": success_message,
            "error_message": error_message,
            "all_likes": getAllLikes(request)
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
        "all_likes": getAllLikes(request)
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
            return render(request, "threadfusion/editanswer.html", {
                "form": form,
                "question_id": question_id,
                "alert": "Answer field cannot be empty"
            })
    else:
        form = AnswerForm(instance=answer)
    return render(request, "threadfusion/editanswer.html", {"form": form})

def tags(request, tag):
    filtered_questions = Question.objects.filter(tags__icontains=tag)

    paginator = Paginator(filtered_questions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    questions = []
    for question in page_obj:
        tags = [t.strip() for t in question.tags.split(",")]
        all_answers = Answer.objects.filter(question=question)
        answers_count = all_answers.count()

        questions.append({
            'question': question,
            'tags': tags,
            'answers_count': answers_count,
        })

    return render(request, "threadfusion/tags.html", {
        "tag": tag,
        "filtered_questions": questions,
        "page_obj": page_obj,
    })

def search(request):
    query = request.GET.get('q', '').strip()
    questions = Question.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(tags__icontains=query)
    )

    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    searched_questions = []
    for question in page_obj:
        tags = [t.strip() for t in question.tags.split(",")]
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
        "searched_questions": searched_questions,
        "page_obj": page_obj
    })

def userprofile(request, id):
    user = User.objects.get(pk=id)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    following = Follow.objects.filter(follower=user)
    followers = Follow.objects.filter(being_followed=user)
    questions = Question.objects.filter(user=user)
    answers = Answer.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)

    try:
        ifFollowing = followers.filter(follower=User.objects.get(pk=request.user.id))
        if len(ifFollowing) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False

    return render(request, "threadfusion/profile.html", {
        "profile_user": user,
        "profile": profile,
        "following": following,
        "followers": followers,
        "isFollowing": isFollowing,
        "questions": questions,
        "answers": answers,
        "comments": comments,
    })

def follow(request):
    profile_user = request.POST['profileUser']
    current_user = User.objects.get(pk=request.user.id)
    profile_user_data = User.objects.get(username=profile_user)
    follows = Follow(follower=current_user, being_followed=profile_user_data)
    follows.save()
    user_id = profile_user_data.id
    return HttpResponseRedirect(reverse('userprofile', kwargs={'id': user_id}))

def unfollow(request):
    profile_user = request.POST['profileUser']
    current_user = User.objects.get(pk=request.user.id)
    profile_user_data = User.objects.get(username=profile_user)
    follows = Follow.objects.get(follower=current_user, being_followed=profile_user_data)
    follows.delete()
    user_id = profile_user_data.id
    return HttpResponseRedirect(reverse('userprofile', kwargs={'id': user_id}))

def updateprofile(request, id):
    if not request.user.is_authenticated and request.user.id != id:
        return HttpResponseRedirect(reverse('index'))
    
    user = get_object_or_404(User, pk=id)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            form = ProfileForm()
            return render(request, 'threadfusion/updateprofile.html', {
                "form": form,
                "user_id": user.id,
                "alert": "Profile updated successfully"
            })
    else:
        form = ProfileForm(instance=profile)
    context = {'form': form, 'user': user}
    return render(request, "threadfusion/updateprofile.html", context)

def userassets(request, id, asset):
    user = User.objects.get(pk=id)
    context = { "user": user, "asset": asset }

    if (asset == 'questions'):
        user_questions = Question.objects.filter(user=user)
        paginator = Paginator(user_questions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        questions = []
        for question in page_obj:
            tags = [t.strip() for t in question.tags.split(",")]
            all_answers = Answer.objects.filter(question=question)
            answers_count = all_answers.count()

            questions.append({
                'question': question,
                'tags': tags,
                'answers_count': answers_count,
            })

        context.update({
            "user_questions": questions,
            "page_obj": page_obj
        })

    elif asset == 'answers':
        user_answers = Answer.objects.filter(user=user)
        paginator = Paginator(user_answers, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        answers = []
        for answer in page_obj:
            question = answer.question

            answers.append({
                'answer': answer,
                'question': question,
            })

        context.update({
            "user_answers": answers,
            "page_obj": page_obj
        })

    elif asset == 'comments':
        user_comments = Comment.objects.filter(user=user)
        paginator = Paginator(user_comments, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        comments = []
        for comment in page_obj:
            question = comment.question
            answer = comment.answer

            comments.append({
                'comment': comment,
                'question': question,
                'answer': answer,
            })

        context.update({
            "user_comments": comments,
            "page_obj": page_obj
        })
    return render(request, "threadfusion/userAssets.html", context)

def getAllLikes(request):
    if request.user.is_authenticated:
        all_likes = []
        likes = Like.objects.all().filter(user = request.user)
        for like in likes:
            all_likes.append(like.answer.id)
        return all_likes
    else:
        return []
    
@csrf_exempt
def like(request):
    if request.method != 'PUT':
        return JsonResponse({
            "error": "PUT request is required"
        }, status = 400)

    answer_request = json.loads(request.body)

    action = answer_request.get("action", "")
    answer_id = answer_request.get("answer_id", "")

    try:
        get_answer = Answer.objects.get(pk=answer_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Answer not found!"}, status = 400)

    if action == 'like':

        if get_answer.id in getAllLikes(request):
             #Unlike this Answer
             remove_like = Like.objects.filter(user = request.user, answer = get_answer)
             remove_like.delete()
             return JsonResponse({"message": "Like has been removed!"}, status = 200)
        else:
            #Like this Answer
            like_answer = Like.objects.create(
                user = request.user,
                answer = get_answer
            )
            like_answer.save()
            return JsonResponse({"message": "Answer liked!"}, status = 201)
    else:
        return JsonResponse({"error": 'Incorrect action!'}, status = 400)