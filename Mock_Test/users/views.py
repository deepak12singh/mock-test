# from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
# from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
# from django.contrib import messages
# from django.contrib.messages.views import SuccessMessageMixin
# from django.views import View
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import views as auth_views
# from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
# from django.core.mail import send_mail



# class CustomLogoutView(auth_views.LogoutView):
#     http_method_names = ['get', 'post']
#     next_page = reverse_lazy('home')

# class RegisterView(View):
#     form_class = RegisterForm
#     initial = {'key': 'value'}
#     template_name = 'users/register.html'

#     def dispatch(self, request, *args, **kwargs):
#         # will redirect to the home page if a user tries to access the register page while logged in
#         if request.user.is_authenticated:
#             return redirect(to='/')

#         # else process dispatch as it otherwise normally would
#         return super(RegisterView, self).dispatch(request, *args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)

#         if form.is_valid():
#             form.save()

#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}')

#             return redirect(to='login')

#         return render(request, self.template_name, {'form': form})


# # Class based view that extends from the built in login view to add a remember me functionality
# class CustomLoginView(LoginView):
#     form_class = LoginForm

#     def form_valid(self, form):
#         remember_me = form.cleaned_data.get('remember_me')

#         if not remember_me:
#             # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
#             self.request.session.set_expiry(0)

#             # Set session as modified to force data updates/cookie to be saved.
#             self.request.session.modified = True

#         # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
#         return super(CustomLoginView, self).form_valid(form)


# class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
#     template_name = 'users/password_reset.html'
#     email_template_name = 'users/password_reset_email.html'
#     subject_template_name = 'users/password_reset_subject'
#     success_message = "We've emailed you instructions for setting your password, " \
#                       "if an account exists with the email you entered. You should receive them shortly." \
#                       " If you don't receive an email, " \
#                       "please make sure you've entered the address you registered with, and check your spam folder."
#     success_url = reverse_lazy('home')


# class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
#     template_name = 'users/change_password.html'
#     success_message = "Successfully Changed Your Password"
#     success_url = reverse_lazy('home')


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         user_form = UpdateUserForm(request.POST, instance=request.user)
#         profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile is updated successfully')
#             return redirect(to='users-profile')
#     else:
#         user_form = UpdateUserForm(instance=request.user)
#         profile_form = UpdateProfileForm(instance=request.user.profile)

#     return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

# Class based view that extends from the built in login view to add a remember me functionality
# class CustomLoginView(LoginView):
#     form_class = LoginForm

#     def form_valid(self, form):
#         remember_me = form.cleaned_data.get('remember_me')

#         if not remember_me:
#             # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
#             self.request.session.set_expiry(0)

#             # Set session as modified to force data updates/cookie to be saved.
#             self.request.session.modified = True

#         # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
#         return super(CustomLoginView, self).form_valid(form)


# class OTPVerificationView(View):
#     template_name = 'users/verify_otp.html'

#     def get(self, request, user_id):
#         return render(request, self.template_name, {'user_id': user_id})

#     def post(self, request, user_id):
#         otp = request.POST.get('otp')
#         user = get_object_or_404(User, id=user_id)
#         profile = Profile.objects.get(user=user)

#         if profile.otp_code == otp and profile.is_otp_valid():
#             profile.otp_code = None  # Clear OTP after verification
#             profile.otp_created_at = None
#             profile.is_verified = True  # Mark user as verified
#             profile.save()
#             messages.success(request, "OTP verified successfully! You can now log in.")
#             return redirect('login')
#         else:
#             messages.error(request, "Invalid or expired OTP.")
#             return render(request, self.template_name, {'user_id': user_id})


from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from .utils import create_and_send_otp
from django.contrib.auth.models import User
from .models import Profile

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()

            # Ensure profile is only created if it does not exist
            profile, created = Profile.objects.get_or_create(user=user)

            create_and_send_otp(user)  # Send OTP after successful registration
            return redirect('verify_otp', user_id=user.id)

        return render(request, self.template_name, {'form': form})



class OTPVerificationView(View):
    template_name = 'users/verify_otp.html'

    def dispatch(self, request, user_id, *args, **kwargs):
        """Agar OTP verified hai toh login page par redirect karo."""
        try:
            user = User.objects.get(id=user_id)
            profile = Profile.objects.get(user=user)

            if profile.is_verified:
                return redirect('login')  # OTP verified toh login bhej do

        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('login')

        return super().dispatch(request, user_id, *args, **kwargs)

    def get(self, request, user_id):
        """GET request ke liye OTP verification page dikhao."""
        return render(request, self.template_name, {'user_id': user_id})

    def post(self, request, user_id):
        """User ka OTP check karo aur verify karo."""
        otp = request.POST.get('otp')

        try:
            user = User.objects.get(id=user_id)
            profile = Profile.objects.get(user=user)

            if profile.otp_code == otp and profile.is_otp_valid():
                profile.is_verified = True  # Mark OTP as verified
                profile.otp_code = None
                profile.otp_created_at = None
                profile.save()

                messages.success(request, "OTP verified successfully! Please log in.")
                return redirect('login')

            else:
                messages.error(request, "Invalid or expired OTP.")
                return render(request, self.template_name, {'user_id': user_id})

        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('login')

class ResendOTPView(View):
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        create_and_send_otp(user)
        messages.success(request, "New OTP sent to your email!")
        return redirect('verify_otp', user_id=user_id)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})




    
class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        profile = Profile.objects.get(user=user)
        print(profile.is_verified)

        if not profile.is_verified:
            messages.error(self.request, "Please verify your OTP before logging in.")
            return redirect('verify_otp', user_id=user.id)  # Redirect to OTP verification page

        return super().form_valid(form)
    


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')


class CustomLogoutView(auth_views.LogoutView):
    http_method_names = ['get', 'post']
    next_page = reverse_lazy('home')