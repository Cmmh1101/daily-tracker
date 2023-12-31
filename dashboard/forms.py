from django import forms
from .models import CATEGORY_CHOICES, Activity, Goal
from django.core.validators import MinValueValidator

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
    target_date = forms.DateField(
        label='Target Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Goal
        fields = ['title', 'type', 'category', 'description', 'actions', 'target_date']

    # Add validation to fields
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    widgets = {
        'title': forms.TextInput(attrs={'class': 'w-full bg-blue-500 border p-5 rounded'}),
        'type': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
        'category': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
        'description': forms.Textarea(attrs={'class': 'w-full border p-2 rounded'}),
        'actions': forms.Textarea(attrs={'class': 'w-full border p-2 rounded'}),
    }

class DateSelectionForm(forms.Form):
    year = forms.IntegerField(
        label='Year',
        widget=forms.NumberInput(attrs={'placeholder': 'YYYY'}),validators=[MinValueValidator(2023)]
        )
    
    month = forms.IntegerField(
        label='Month', 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'MM'}), validators=[MinValueValidator(1)]
        )
    
    day = forms.IntegerField(
        label='Day', 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'DD'}), validators=[MinValueValidator(1)]
        )
    
    category = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )