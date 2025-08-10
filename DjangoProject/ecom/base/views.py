from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Mentor, Availability, Booking
from .forms import StudentRegisterForm, MentorAvailabilityForm, BookingForm
from .emails import send_booking_emails
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import uuid

from django.utils.dateparse import parse_datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Mentor, Booking
from .forms import BookingForm
from .emails import send_booking_emails
import uuid
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import uuid
from .models import Mentor
from .forms import BookingForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Mentor
from .forms import BookingForm
from django.utils import timezone
from .emails import send_booking_emails
import uuid
from django.contrib.auth.decorators import login_required

def student_register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.save()
            login(request, user)
            return redirect('mentor_list')
    else:
        form = StudentRegisterForm()
    return render(request, 'registration/register.html', {'form': form})



def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # ✅ This logs the user in
            return redirect('mentor_list')  # or use request.GET.get('next', 'mentor_list')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'registration/login.html')



def mentor_list(request):
    mentors = Mentor.objects.all()
    return render(request, 'mentorship/mentor_list.html', {'mentors': mentors})




@login_required
def mentor_availability(request):
    if not hasattr(request.user, 'mentor_profile'):
        return redirect('mentor_list')
    if request.method == 'POST':
        form = MentorAvailabilityForm(request.POST)
        if form.is_valid():
            av = form.save(commit=False)
            av.mentor = request.user.mentor_profile
            av.save()
            messages.success(request, "Availability added")
            return redirect('mentor_availability')
    else:
        form = MentorAvailabilityForm()
    my_avail = request.user.mentor_profile.availabilities.all()
    return render(request, 'mentorship/mentor_availability.html', {'form': form, 'availabilities': my_avail})

def home(request):
    return render(request, 'home.html')


def mentor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'mentor_profile'):
            login(request, user)
            return redirect('mentor_availability')  # Redirect to mentor dashboard
        else:
            messages.error(request, 'Invalid credentials or not a mentor.')
    return render(request, 'registration/mentor_login.html')


@login_required
def mentor_detail(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    availabilities = Availability.objects.filter(mentor=mentor)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        slot_value = request.POST.get('slot')  # e.g., "2025-08-06T10:00|2025-08-06T10:30"

        if slot_value:
            start_str, end_str = slot_value.split('|')
            start = parse_datetime(start_str)
            end = parse_datetime(end_str)

            # manually create booking without form.save()
            booking = Booking.objects.create(
                mentor=mentor,
                student=request.user,
                start=start,
                end=end,
                paid=mentor.is_paid,
                meeting_link="https://your-meeting-link.com"
            )

            send_booking_emails(booking)  # Send email after booking

            if mentor.is_paid:
                return redirect('payment_page', booking_id=booking.id)
            else:
                return redirect('booking_success')

        else:
            messages.error(request, "Please select a valid time slot.")
    else:
        form = BookingForm()

    return render(request, 'mentorship/mentor_detail.html', {
        'mentor': mentor,
        'availabilities': availabilities,
        'form': form,
    })




@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, student=request.user)
    return render(request, 'mentorship/payment_page.html', {'booking': booking})


@login_required
def confirm_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, student=request.user)
    if request.method == 'POST':
        booking.paid = True
        booking.save()
        send_booking_emails(booking)
        return redirect('booking_success')

def booking_success(request):
    return render(request, 'mentorship/booking_success.html')
