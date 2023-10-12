from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("activities", views.activities_view, name="activities"),
    path("goals", views.goals_view, name="goals"),
    path("addActivity", views.addActivity_view, name="addActivity"),
    path("addGoal", views.addGoal_view, name="addGoal")
]
