import random
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Profile

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user, otp):
    subject = "Your OTP Code"
    message = f"Your OTP is {otp}. It is valid for 5 minutes."
    print(message)
    send_mail(subject, message, "deepaksingh@gmail.com", [user.email])

def create_and_send_otp(user):
    otp = generate_otp()
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.otp_code = otp
    profile.otp_created_at = now()
    profile.save()
    send_otp_email(user, otp)
