from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("activities", views.activities_view, name="activities"),
    path("activities/<int:activity_id>", views.activity_view, name="activity"),
    path("goals", views.goals_view, name="goals"),
    path("goals/<int:goal_id>", views.goal_view, name="goal"),
    path("addActivity", views.addActivity_view, name="addActivity"),
    path("addGoal", views.addGoal_view, name="addGoal"),
    path("editActivity/<int:activity_id>", views.edit_activity, name="editActivity"),
    path("editGoal/<int:goal_id>", views.editGoal_view, name="editGoal"),
    path("deleteActivity/<int:activity_id>", views.delete_activity, name="deleteActivity"),
    path("deleteGoal/<int:goal_id>", views.delete_goal, name="deleteGoal"),
    path('generate_pdf/<int:year>/<int:month>/', views.generate_pdf_report, name='generate_pdf_report')
]
