# from django.db import models
# from django.contrib.auth.models import User
# from PIL import Image


# # Extending User Model Using a One-To-One Link
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
#     bio = models.TextField()

#     def __str__(self):
#         return self.user.username

#     # resizing images
#     def save(self, *args, **kwargs):
#         super().save()

#         img = Image.open(self.avatar.path)

#         if img.height > 100 or img.width > 100:
#             new_img = (100, 100)
#             img.thumbnail(new_img)
#             img.save(self.avatar.path)

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.timezone import now, timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    is_verified = models.BooleanField(default=False)  # Add this field
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    # OTP Validity Check
    def is_otp_valid(self):
        if self.otp_created_at:
            return now() <= self.otp_created_at + timedelta(minutes=5)  # Valid for 5 minutes
        return False

    # Resizing images
    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            img.thumbnail((100, 100))
            img.save(self.avatar.path)
