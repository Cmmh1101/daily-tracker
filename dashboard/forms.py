from django import forms
from .models import Activity, Goal

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'linked_goals']

    # Add validation to fields
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    # Customize widgets with Tailwind CSS classes
    widgets = {
        'title': forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
        'description': forms.Textarea(attrs={'class': 'w-full border p-2 rounded'}),
        'linked_goals': forms.SelectMultiple(attrs={'class': 'w-full border p-2 rounded'}),
    }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'type', 'category', 'summary', 'description', 'actions']

    def __init__(self, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)