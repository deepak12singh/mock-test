from django.urls import path
from . import views

urlpatterns = [
    path('cuet_pg/', views.cuet_pg, name='cuet_pg'),
    path('cuet_ug/', views.cuet_ug, name='cuet_ug'),
    path('exam_tips/', views.exam_tips, name='exam_tips'),
    path('participating_university/', views.participating_university, name='participating_university'),
    path('pg_exam_details/', views.pg_exam_details, name='pg_exam_details'),
    path('pg_syllabus/', views.pg_syllabus, name='pg_syllabus'),
    path('PGFAQ/', views.PGFAQ, name='PGFAQ'),
    path('ug_exam_details/', views.ug_exam_details, name='ug_exam_details'),
    path('ug_syllabus/', views.ug_syllabus, name='ug_syllabus'),
    path('UGFAQ/', views.UGFAQ, name='UGFAQ'),
]
