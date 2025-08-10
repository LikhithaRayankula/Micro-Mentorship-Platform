from django.core.mail import send_mail
from django.conf import settings

def send_booking_emails(booking):
    subject = "Mentorship Session Confirmation"
    message = f"""
Hi {booking.student.first_name},

Your session with mentor {booking.mentor.name} has been successfully booked!

🔹 Mentor: {booking.mentor.name}
🔹 Qualification: {booking.mentor.qualification}
🔹 Role: {booking.mentor.job_role}
🔹 Date & Time: {booking.start.strftime('%A, %d %B %Y at %I:%M %p')} to {booking.end.strftime('%I:%M %p')}
🔹 Meeting Link: {booking.meeting_link}

Please be on time. If any issues, contact the support team.

Best regards,  
MicroMentorship Team
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.student.email],
        fail_silently=False,
    )
