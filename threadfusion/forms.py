from django import forms
from .models import Question, Answer, Profile

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

class ProfileForm(forms.ModelForm):
   profile_image = forms.ImageField(label='Upload Image', required=False, widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}))
   fullname = forms.CharField(label='Fullname', widget=forms.TextInput(attrs={'class': 'input-field'}))
   profession = forms.CharField(label='Profession', widget=forms.TextInput(attrs={'class': 'input-field'}))
   linkedin = forms.CharField(label='Linkedin Profile Link', required=False, widget=forms.TextInput(attrs={'class': 'input-field'}))
   github = forms.CharField(label='Github Profile Link', required=False, widget=forms.TextInput(attrs={'class': 'input-field'}))
   instagram = forms.CharField(label='Instagram Profile Link', required=False, widget=forms.TextInput(attrs={'class': 'input-field'}))
   facebook = forms.CharField(label='Facebook Profile Link', required=False, widget=forms.TextInput(attrs={'class': 'input-field'}))
   twitter = forms.CharField(label='Twitter Profile Link', required=False, widget=forms.TextInput(attrs={'class': 'input-field'}))
   class Meta:
      model = Profile
      fields = ['profile_image', 'fullname', 'profession', 'about', 'linkedin', 'github', 'instagram', 'facebook', 'twitter']