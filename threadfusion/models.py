from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Contact(models.Model):
    fullname = models.CharField(max_length=64)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fullname} has sent a message"
    
class Question(models.Model):
    title = models.CharField(max_length=140)
    description = QuillField()
    tags = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question {self.id} posted by {self.user}"
    
class Answer(models.Model):
    answer = QuillField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_answered")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} answered({self.id}) the question({self.question.id}) asked by {self.question.user}"
    
class Comment(models.Model):
    comment = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_commented")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="main_question")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answer_of_comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} commented({self.id}) on Answer {self.answer.id} of Question {self.question.id}"