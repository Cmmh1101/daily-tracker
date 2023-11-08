# Create a new directory for your project
mkdir your_project_name
cd your_project_name

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS and Linux:
source venv/bin/activate

# Install Django
pip install django

# Create a New Django Project
django-admin startproject your_project_name .

# Configure Your Database
pip install psycopg2-binary

Next, open your project's settings.py file and locate the DATABASES section. Update it to use PostgreSQL with your database settings:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',  # or the IP address of your PostgreSQL server
        'PORT': '',           # leave empty for default PostgreSQL port (5432)
    }
}

# Installing django-environ
 python -m pip install django-environ

# Import environ in settings.py and initialize
import environ
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Create your .env file
In the same directory as settings.py, create a file called ‘.env’

Make sure you don’t use quotations around strings.

SECRET_KEY=h^z13$qr_s_wd65@gnj7a=xs7t05$w7q8!x_8zsld#
DATABASE_NAME=postgresdatabase
DATABASE_USER=john
DATABASE_PASS=supersecretpassword

## IMPORTANT: Add your .env file to .gitignore

#  Create a New Django App
python3 manage.py startapp your_app_name

# define your models
 Create the models.py file in your app directory and define your models there.

#  run python manage.py makemigrations and python manage.py migrate

## Errors: 
while trying to makemigrations, I got an auth models error, and solved it by adding this line to my settings.py

AUTH_USER_MODEL="myproject.User"

# Install tailwind

python3 -m pip install django-tailwind

## add tailwind to INSTALLED_APPS settings.py

INSTALLED_APPS = [
  # other Django apps
  'tailwind',
]

## Create a Tailwind CSS compatible Django app, I like to call it theme

python manage.py tailwind init

## Add your newly created 'theme' app to INSTALLED_APPS in settings.py

INSTALLED_APPS = [
  # other Django apps
  'tailwind',
  'theme'
]

## Register the generated 'theme' app by adding the following line to settings.py

TAILWIND_APP_NAME = 'theme'

## Make sure that the INTERNAL_IPS list is present in the settings.py file and contains the 127.0.0.1 ip address:

INTERNAL_IPS = [
    "127.0.0.1",
]

## Install Tailwind CSS dependencies, by running the following command:

python3 manage.py tailwind install

# create templates

# create static folder > dashboard folder > styles.css

# start tailwind

python3 manage.py tailwind start

# add urls to your app and project

# Create your templates and views

# Register your models in admin.py

In the admin.py file, import your models and use the admin.site.register method to register them. 

ex. 
from django.contrib import admin
from .models import User, Activity, Goal

admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Goal)

# setup a custom 404 view

# install django-chartjs

pip install django-chartjs

# add in installed apps

```
INSTALLED_APPS = [
    # ...
    'chartjs',
]
```

# create a view & template


<!-- working pdf -->

<!DOCTYPE html>
<html>
<head>
    <title>Activity Report</title>
    <!-- Add your CSS styles here, including any styling specific for the PDF export -->
</head>
<body>
    <h1>Activity Report for {{ report_date }}</h1>
    <ul>
        {% for activity in activities %}
            <li>{{ activity.title }} - {{ activity.created_at }}</li>
        {% endfor %}
    </ul>
</body>
</html>

## Troubleshooting postgres connection if port in use error
- Run this command to check postgres is the one in use of the port
> $ sudo lsof -i :5432

- Run this command to kill postgres 
> $ sudo pkill -u postgres
