# urls.py
from django.urls import path
from .views import exam_view, submit_exam

urlpatterns = [
    path("exam/", exam_view, name="exam"),
    path("exam/submit/", submit_exam, name="exam_submit"),  # Changed URL name to match template
]
