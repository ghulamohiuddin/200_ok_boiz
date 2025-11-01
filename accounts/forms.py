# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import SeekerProfile, Interest
from .models import FinderProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Use your university email if possible.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_talent_finder", "is_talent_seeker")

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email or Username")

# accounts/forms.py


class SeekerProfileForm(forms.ModelForm):
    # Render the interests as checkboxes
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = SeekerProfile
        fields = ['full_name', 'email', 'university', 'skills', 'interests']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'e.g., Alex Doe'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@university.edu'}),
            'university': forms.TextInput(attrs={'placeholder': 'e.g., Stanford / Computer Science'}),
            'skills': forms.Textarea(attrs={'rows':3, 'placeholder': 'Python, UI/UX Design, ...'}),
        }


class FinderProfileForm(forms.ModelForm):
    class Meta:
        model = FinderProfile
        fields = ['full_name', 'email', 'university', 'organization', 'opportunities']
        widgets = {
            'opportunities': forms.CheckboxSelectMultiple()
        }
