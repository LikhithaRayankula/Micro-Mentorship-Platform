from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Booking, Mentor, Availability

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []  # or use exclude = [...] as above

class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class MentorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['start','end']
