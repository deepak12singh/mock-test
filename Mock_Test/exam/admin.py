# admin.py
from django.contrib import admin
from .models import QuestionUG, QuestionPG

# Register Models
@admin.register(QuestionUG)
class QuestionUGAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'correct_option')
    search_fields = ('question',)
    list_filter = ('correct_option',)

@admin.register(QuestionPG)
class QuestionPGAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'correct_option')
    search_fields = ('question',)
    list_filter = ('correct_option',)

