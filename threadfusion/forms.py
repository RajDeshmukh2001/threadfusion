from django import forms
from .models import Question, Answer

class AskQuestionForm(forms.ModelForm):
   class Meta:
      model = Question
      fields = ['title', 'description', 'tags']
      widgets = {
         'title': forms.TextInput(attrs={'placeholder': 'Be clear and concise in your question title. Your title should summarize the problem.'}),
         'tags': forms.TextInput(attrs={'placeholder': 'Add up to 5 tags separated by commas to describe what your question is about.', 'autocomplete': 'off'}),
      }
      labels = {
         'title': 'Question (Title)',
         'description': 'Explain your question in details',
      }
      help_texts = {
         'title': 'Be clear and concise in your question title. Your title should summarize the problem.',
         'description': 'Explain the problem and expand on what you put in the title. If relevant, include your code. Minimum 20 characters.',
         'tags': 'Add up to 5 tags separated by commas to describe what your question is about.',
      }

class AnswerForm(forms.ModelForm):
   class Meta:
      model = Answer
      fields = ['answer']