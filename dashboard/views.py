from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from dashboard.forms import ActivityForm, GoalForm
from .models import Activity, User, Goal, TYPE_CHOICES, CATEGORY_CHOICES


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
    
    goals = Goal.objects.filter(user=request.user)
    return render(request, "dashboard/goals.html",{
        'goals': goals,
        'categories': CATEGORY_CHOICES,
    })

def goal_view(request, goal_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    return render(request, "dashboard/goal.html", {
        'goal': goal
    })
    

def addActivity_view(request):
    if not request.user.is_authenticated:
            return redirect("login")
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            # Create a new Activity instance and set the user
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()

            # Add the selected goals to the linked_goals field
            selected_goals = form.cleaned_data.get('linked_goals')
            activity.linked_goals.set(selected_goals)

            return redirect('activities')  # Redirect to your activity list view
    else:
        form = ActivityForm()

   
    return render(request, 'dashboard/addActivity.html', {
    'form': ActivityForm(),
    })
    
def edit_activity(request, activity_id):
    if not request.user.is_authenticated:
        return redirect("login")
    activity = get_object_or_404(Activity, id=activity_id, user=request.user)

    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()  # Save the updated form data

        return redirect("activities")

    else:
        form = ActivityForm(instance=activity)

    
    return render(request, "dashboard/editActivity.html", {
        'form': form,
        'activity': activity,
    })
    
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    if request.method == 'POST':
        activity.delete()
        return redirect('activities') 

    return render(request, 'dashboard/deleteActivity.html', {'activity': activity})

def addGoal_view(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user  # Associate the goal with the logged-in user
            goal.save()

            # Redirect to a success page or any other desired action
            return redirect('goals')  
    else:
        form = GoalForm()

    return render(request, 'dashboard/addGoal.html', {
        'form': form,
        'TYPE_CHOICES': TYPE_CHOICES,
        'CATEGORY_CHOICES': CATEGORY_CHOICES,
        })

def custom_404(request, exception):
    return render(request, 'dashboard/404.html', status=404)