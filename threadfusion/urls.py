from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow"),
    path('search/', views.search, name="search"),
    path("login", views.login_view, name="login"),
    path("contact", views.contact, name="contact"),
    path("tags/<str:tag>", views.tags, name="tags"),
    path("logout", views.logout_view, name="logout"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("register", views.register, name="register"),
    path("askquestion", views.askquestion, name="askquestion"),
    path('userprofile/<int:id>', views.userprofile, name="userprofile"),
    path("editquestion/<int:id>", views.editquestion, name="editquestion"),
    path('updateprofile/<int:id>', views.updateprofile, name="updateprofile"),
    path("singlequestion/<int:id>", views.singlequestion, name="singlequestion"),
    path("deletequestion/<int:id>", views.deletequestion, name="deletequestion"),
    path("editanswer/<int:question_id>/<int:answer_id>", views.editanswer, name="editanswer"),
    path("userassets/<int:id>/<str:asset>", views.userassets, name="userassets"),
]