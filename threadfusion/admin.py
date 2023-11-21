from django.contrib import admin
from .models import User, Contact, Question, Answer, Comment

admin.site.register(User)
admin.site.register(Answer)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(Question)