from django.db import models
from django.contrib.auth.models import User
import json

class ResultAnswer(models.Model):
    question_id = models.IntegerField()
    index = models.IntegerField()
    exam_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    ug_or_pg = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    selected_option = models.CharField(max_length=10)
    marks = models.IntegerField()

    # ✅ Time field
    created_at = models.DateTimeField(auto_now_add=True)  # automatically set on creation
    # updated_at = models.DateTimeField(auto_now=True)      # automatically updates on save

    def __str__(self):
        return f"{self.user.username} - {self.exam_name} - Q{self.index}"


class ResultNotAttempt(models.Model):
    exam_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    ug_or_pg = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Store question indices as JSON in text field
    question_indices = models.TextField(blank=True, null=True)

    # ✅ Time field
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    marks = models.IntegerField()

    def set_question_indices(self, indices_dict):
        self.question_indices = json.dumps(indices_dict)
        
    def get_question_indices(self):
        if self.question_indices:
            return json.loads(self.question_indices)
        return {}
        
    def __str__(self):
        return f"{self.user.username} - {self.exam_name}"
