from django.contrib import admin
from .models import User, Question, Answer, Comment, Profile, Follow, Like, Contact

admin.site.register(User)
admin.site.register(Like)
admin.site.register(Answer)
admin.site.register(Follow)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Question)