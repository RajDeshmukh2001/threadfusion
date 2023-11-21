from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("contact", views.contact, name="contact"),
    path("register", views.register, name="register"),
    path("askquestion", views.askquestion, name="askquestion"),
    path("singlequestion/<int:id>", views.singlequestion, name="singlequestion"),
    path("editquestion/<int:id>", views.editquestion, name="editquestion"),
    path("deletequestion/<int:id>", views.deletequestion, name="deletequestion"),
    path("editanswer/<int:question_id>/<int:answer_id>", views.editanswer, name="editanswer"),
    path("tags/<str:tag>", views.tags, name="tags"),
    path('search/', views.search, name="search"),
]