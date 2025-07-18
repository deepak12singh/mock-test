from django.urls import path
from django.contrib.auth import views as auth_views
from .views import profile, RegisterView, CustomLoginView, ResetPasswordView, ChangePasswordView, CustomLogoutView, OTPVerificationView, ResendOTPView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='users-register'),
    path('verify-otp/<int:user_id>/', OTPVerificationView.as_view(), name='verify_otp'),
    path('resend-otp/<int:user_id>/', ResendOTPView.as_view(), name='resend_otp'),

    path('profile/', profile, name='users-profile'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # Password reset URLs
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]
