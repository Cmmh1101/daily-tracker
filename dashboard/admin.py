from django.contrib import admin
from .models import User, Activity, Goal

# Register your models here.
admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Goal)
