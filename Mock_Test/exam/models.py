from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class QuestionUG(models.Model):
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')],
        validators=[RegexValidator(regex='^[A-D]$', message="Correct option must be A, B, C, or D.")]
    )
    subject = models.CharField(
    max_length=255,
    choices=[
        ("Physics", "Physics"),
        ("Chemistry", "Chemistry"),
        ("Mathematics", "Mathematics"),
        ("Biology", "Biology"),
        ("English", "English"),
    ],
    default="Physics"  
    )

    def __str__(self):
        return self.question


class QuestionPG(models.Model):
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    subject = models.CharField(
    max_length=255,
    choices=[("MBA", "MBA"), ("MCA", "MCA"), ("MA English", "MA English"), ("MA Hindi", "MA Hindi"),("M.Com", "M.Com")],
    default="MBA"  
    )
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')],
        validators=[RegexValidator(regex='^[A-D]$', message="Correct option must be A, B, C, or D.")]
    )
    main_subject = models.CharField(
    max_length=255,
    choices=[
        ("Hindi","Hindi"),
        ("English", "English"),
        ("Mathematics", "Mathematics"),
        ("Reasoning","Reasoning"),
        ("Computer","Computer"),
        ("Micro Ecomonics","Micro Ecomonics"),
        ("Currency and banking","Currency and banking"),
        ("Accounting","Accounting"),
        ("Company law","Company law"),
        ("Business maths","Business maths"),
        ("Indian writing","Indian writing"),
        ("Literary terms","Literary terms"),
        ("Literary genres","Literary genres"),
        ("Literary criticism","Literary criticism"),
        ("Rachnakar","Rachnakar"),
        ("Kaal vibhajan","Kaal vibhajan"),
        ("Jansanchar madhya","Jansanchar madhya"),
        ("Kavya shastra","Kavya shastra"),
        ("Vyakaran","Vyakaran")
    ],
    default="English"  
    )

    def __str__(self):
        return self.question

