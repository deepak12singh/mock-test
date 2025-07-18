from django.urls import path
from . import views

app_name = "exam_results"

urlpatterns = [
    path('history/', views.test_history_view, name='test_history'),
    path('detail/<str:exam_name>/<str:subject>/<str:ug_or_pg>/', views.result_detail_view, name='test_result_detail'),
]
