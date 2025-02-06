from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Registration Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Login Form
class LoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']

# PROFILE FORMS
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class InfiniteFlightDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['infinite_flight_username']

    def clean_infinite_flight_username(self):
        username = self.cleaned_data.get('infinite_flight_username')
        if Profile.objects.filter(infinite_flight_username=username).exists():
            raise forms.ValidationError("This Infinite Flight username is already in use.")
        return username

class MembershipTestForm(forms.Form):
    # Add fields related to the membership test (this can be questions/answers or a quiz)
    question1 = forms.CharField(max_length=100, label="What is your favorite flight route?")
    question2 = forms.CharField(max_length=100, label="What is the maximum altitude for your aircraft?")

class FlightReplayForm(forms.Form):
    flight_replay = forms.FileField(label="Upload Flight Replay")
