from django import forms
from .models import Activity, Goal

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'linked_goal']

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
        'linked_goal': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
    }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'type', 'category', 'description', 'actions']

    # Add validation to fields
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    # Customize widgets with Tailwind CSS classes
    widgets = {
        'title': forms.TextInput(attrs={'class': 'w-full bg-blue-500 border p-5 rounded'}),
        'type': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
        'category': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
        'description': forms.Textarea(attrs={'class': 'w-full border p-2 rounded'}),
        'actions': forms.Textarea(attrs={'class': 'w-full border p-2 rounded'}),
    }

class DateSelectionForm(forms.Form):
    year = forms.IntegerField(label='Year', required='False', widget=forms.SelectDateWidget(years=range(2023, 2030)))
    month = forms.IntegerField(label='Month', required='False', widget=forms.SelectDateWidget(months={1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}, required=False))
    day = forms.IntegerField(label='Day', required=False)