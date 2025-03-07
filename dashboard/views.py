from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, F
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import requests
from dashboard.forms import ActivityForm, DateSelectionForm, GoalForm
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dashboard.utils import get_quote
from .models import Activity, User, Goal, CATEGORY_CHOICES

# Create your views here.
def index(request):
    quote_data = get_quote()

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    # total categories
    total_categories = len(CATEGORY_CHOICES)
    
    # total goals by category
    goals_by_category = (
        Goal.objects.filter(user=request.user).values('category')
        .annotate(total=Count('category'))
        .order_by('category')
    )

    # total activities by category
    activities_by_category = (
        Activity.objects.filter(user=request.user).values('linked_goal__category')
        .annotate(total=Count('linked_goal__category'))
        .order_by('linked_goal__category')
    )

    activities_by_goal = (
        Activity.objects.filter(user=request.user).values('linked_goal__id', 'linked_goal__title', 'linked_goal__category')
        .annotate(total=Count('linked_goal__id'))
        .order_by('linked_goal__id')
    )

    context = {
        'total_categories': total_categories,
        'goals_by_category': goals_by_category,
        'activities_by_category': activities_by_category,
        'activities_by_goal': activities_by_goal,
        'quote_data': quote_data
    }

    return render(request, '../templates/index.html', context)

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
            return render(request, "../templates/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "../templates/login.html")


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
            return render(request, "../templates/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "../templates/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "../templates/register.html")
    
CATEGORY_CHOICES = [
    ('professional', 'Professional'),
    ('personal', 'Personal'),
    ('development', 'Development'),
    ('faith', 'Faith'),
    ('financial', 'Financial'),
]

def activities_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    quote_data = get_quote()
    
    filter_category = request.GET.get('category')
    filter_goal = request.GET.get('goal')
    filter_date = request.GET.get('date')
    sort_by = request.GET.get('sort')

    activities = Activity.objects.filter(user=request.user).prefetch_related('linked_goal').order_by('-created_at')

    goals = Goal.objects.filter(user=request.user)

    # Apply category filter
    if filter_category and filter_category != 'all':
        activities = activities.filter(linked_goal__category=filter_category)

    # Apply goal filter
    if filter_goal:
        activities = activities.filter(linked_goal__title=filter_goal)

    # Apply date filter
    if filter_date:
        try:
            filter_date = timezone.datetime.strptime(filter_date, '%Y-%m')
            activities = activities.filter(created_at__year=filter_date.year, created_at__month=filter_date.month)
        except ValueError:
            pass  # Handle invalid date format gracefully, or you can raise an error

    if sort_by:
        if sort_by == 'oldest':
            activities = activities.order_by('created_at')
        elif sort_by == 'newest':
            activities = activities.order_by('-created_at')
    
    return render(request, "../templates/activities.html", {
        'activities': activities,
        'categories': CATEGORY_CHOICES,
        'goals': goals,
        'quote_data': quote_data,  
    })

def activity_view(request, activity_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    quote_data = get_quote()

    activity = get_object_or_404(Activity, id=activity_id, user=request.user)
    return render(request, "../templates/activity.html", {
        'activity': activity,
        'quote_data': quote_data,
    })
    
def goals_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    quote_data = get_quote()

    # Get filter parameters
    filter_status = request.GET.get('status')
    filter_category = request.GET.get('category')

    # Start with all goals
    goals = Goal.objects.filter(user=request.user).order_by('-created_at')

    # Apply status filter
    if filter_status and filter_status != 'all':
        goals = goals.filter(status=filter_status)
    
    # Apply category filter
    if filter_category and filter_category != 'all':
        goals = goals.filter(category=filter_category)

    # Get activities count by goal
    activities_by_goal = (
        Activity.objects.filter(user=request.user).values('linked_goal__id', 'linked_goal__title', 'linked_goal__category')
        .annotate(total=Count('linked_goal__id'))
        .order_by('linked_goal__id')
    )

    return render(request, "../templates/goals.html", {
        'goals': goals,
        'categories': CATEGORY_CHOICES,
        'activities_by_goal': activities_by_goal,
        'quote_data': quote_data,
    })

def goal_view(request, goal_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    quote_data = get_quote()

    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    return render(request, "../templates/goal.html", {
        'goal': goal,
        'quote_data': quote_data,
    })
    

def addActivity_view(request):
    if not request.user.is_authenticated:
            return redirect("login")
    
    quote_data = get_quote()

    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            # Create a new Activity instance and set the user
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()

            # Add the selected goals to the linked_goal field
            goal_id = request.POST.get('linked_goal', None)
            if goal_id:
                goal = Goal.objects.get(pk=goal_id)
                activity.linked_goal = goal
                goal.status = 'In Progress'
                goal.save()

            activity.save()

            return redirect('activities')
    else:
        form = ActivityForm()

    return render(request, '../templates/addActivity.html', {
    'form': ActivityForm(),
    'quote_data': quote_data,
    })
    
def edit_activity(request, activity_id):
    if not request.user.is_authenticated:
        return redirect("login")
    
    quote_data = get_quote()

    activity = get_object_or_404(Activity, id=activity_id, user=request.user)

    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()  # Save the updated form data

        return redirect("activities")

    else:
        form = ActivityForm(instance=activity)

    
    return render(request, "../templates/editActivity.html", {
        'form': form,
        'activity': activity,
        'quote_data': quote_data,
    })
    
def delete_activity(request, activity_id):
    quote_data = get_quote()

    activity = get_object_or_404(Activity, id=activity_id)

    if request.method == 'POST':
        activity.delete()
        return redirect('activities') 

    return render(request, '../templates/deleteActivity.html', {
        'activity': activity,
        'quote_data': quote_data
        })

def addGoal_view(request):

    quote_data = get_quote()

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

    return render(request, '../templates/addGoal.html', {
        'form': form,
        'quote_data': quote_data,
    })

def editGoal_view(request, goal_id):
    quote_data = get_quote()

    goal = get_object_or_404(Goal, id=goal_id)

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            edited_goal = form.save(commit=False)
            edited_goal.user = request.user
            edited_goal.save()

            return redirect('goals')
    else:
        form = GoalForm(instance=goal)

    return render(request, '../templates/editGoal.html', {
        'form': form,
        'goal': goal,
        'quote_data': quote_data,
    })

def delete_goal(request, goal_id):
    quote_data = get_quote()

    goal = get_object_or_404(Goal, id=goal_id)

    if request.method == 'POST':
        goal.delete()
        return redirect('goals') 
    else:
        return render(request, '../templates/deleteGoal.html', {
            'goal': goal,
            'quote_data': quote_data,
            })
    
def generate_pdf_report(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            day = form.cleaned_data['day']
            categories = form.cleaned_data.get('category', [])

            activities = Activity.objects.filter(user=request.user, created_at__year=year)

            if month is not None:
                activities = activities.filter(created_at__month=month)

            if day is not None: 
                activities = activities.filter(created_at__month=month, created_at__day=day)
            
            if categories:
                activities = activities.filter(linked_goal__category__in=categories)

            activities = activities.order_by('created_at')

            if not year:
                return HttpResponseNotFound("Year is required.")

            filename = f'activity_report_{year}'
            if month:
                filename += f'_{month:02d}'
            if day:
                filename += f'_{day:02d}'
            if categories:
                for category in categories:
                    filename += f'_{category}'
            filename += '.pdf'

            # Render the PDF with context using the PDF template
            template = get_template('../templates/pdf_report_template.html')

            context = {
                'activities': activities,
                'report_date': datetime(year, month or 1, day or 1),
                'categories': categories
            }
            html = template.render(context)

            # create pdf response
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename={filename}'

            # Generate the PDF
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    else:
        form = DateSelectionForm()
        quote_data = get_quote()
    
    return render(request, '../templates/generateReport.html', {
        'form': form,
        "quote_data": quote_data,
        })


def custom_404(request, exception):
    return render(request, '/404.html', status=404)

def mark_goal_completed(request, goal_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        goal.status = 'Achieved'
        goal.achieved_at = timezone.now()
        goal.save()
        return redirect('goal', goal_id=goal.id)