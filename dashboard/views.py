from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Activity, User, Goal


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "dashboard/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "dashboard/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "dashboard/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "dashboard/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "dashboard/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "dashboard/register.html")
    
CATEGORY_CHOICES = [
    ('professional', 'Professional'),
    ('personal', 'Personal'),
    ('development', 'Development'),
    ('spiritual', 'Spiritual'),
    ('faith', 'Faith'),
    ('charity', 'Charity'),
]

def activities_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    # Retrieve activities for the current user with linked goals
    activities = Activity.objects.filter(user=request.user).prefetch_related('linked_goals')
    
    return render(request, "dashboard/activities.html", {
        'activities': activities,
        'categories': CATEGORY_CHOICES,
    })

def activity_view(request, activity_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    # get_object_or_404 ensures the activity exists, and that the activity belongs to the currently authenticated user.
    activity = get_object_or_404(Activity, id=activity_id, user=request.user)
    return render(request, "dashboard/activity.html", {
        'activity': activity
    })
    

def goals_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "dashboard/goals.html")

def addActivity_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        linked_goals = request.POST.getlist("linked_goals")

        if title and description:
            # Create a new activity
            activity = Activity(user=request.user, title=title, description=description)
            activity.save()

            # Add linked goals to the activity
            for goal_id in linked_goals:
                try:
                    goal = Goal.objects.get(id=goal_id)
                    activity.linked_goals.add(goal)
                except Goal.DoesNotExist:
                    # Handle the case where a selected goal does not exist
                    pass

            return redirect("activities")  # Redirect to the activities page or a success page
        else:
            # Handle the case where title and description are not provided
            return render(request, "dashboard/addActivity.html", {
                'goals': Goal.objects.filter(user=request.user),
                'error_message': "Title and description are required fields."
            })
    else:
        if not request.user.is_authenticated:
            return redirect("login")

        goals = Goal.objects.filter(user=request.user)
        return render(request, "dashboard/addActivity.html", {
            'goals': goals
        })
    
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, user=request.user)

    if request.method == 'POST':
        title = request.POST.get("title")
        description = request.POST.get("description")
        linked_goals = request.POST.getlist("linked_goals")

        # update edited activity fields
        activity.title = title
        activity.description = description
        activity.save()

        # add linked goals to activity
        activity.linked_goals.clear()
        for goal_id in linked_goals:
            try:
                goal = Goal.objects.get(id=goal_id)
                activity.linked_goals.add(goal)
            except Goal.DoesNotExist:
                # Handle the case where a selected goal does not exist
                pass

        return redirect("activities")

    else:
        if not request.user.is_authenticated:
            return redirect("login")
        return render(request, "dashboard/editActivity.html", {
            "activity": activity,
            "goals": Goal.objects.filter(user=request.user) 
        })
    
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    if request.method == 'POST':
        activity.delete()
        return redirect('activities') 

    return render(request, 'dashboard/deleteActivity.html', {'activity': activity})


def addGoal_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "dashboard/addGoal.html")

def custom_404(request, exception):
    return render(request, 'dashboard/404.html', status=404)