from django.contrib import admin
from .models import ResultAnswer,ResultNotAttempt

# Register your models here.




@admin.register(ResultAnswer)
class ResultAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam_name', 'subject', 'index', 'is_correct', 'selected_option','marks')
    list_filter = ('exam_name', 'subject', 'ug_or_pg', 'is_correct')
    search_fields = ('user__username', 'exam_name', 'subject')


@admin.register(ResultNotAttempt)
class ResultNotAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam_name', 'subject', 'ug_or_pg')
    list_filter = ('exam_name', 'subject', 'ug_or_pg')
    search_fields = ('user__username', 'exam_name', 'subject')