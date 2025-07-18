from django.shortcuts import render



def cuet_pg(request):
    return render(request, 'home/cuet_pg.html')

def cuet_ug(request):
    return render(request, 'home/cuet_ug.html')

def exam_tips(request):
    return render(request, 'home/exam_tips.html')

def participating_university(request):
    return render(request, 'home/participating_university.html')

def pg_exam_details(request):
    return render(request, 'home/pg_exam_details.html')

def pg_syllabus(request):
    return render(request, 'home/pg_syllabus.html')

def PGFAQ(request):
    return render(request, 'home/PGFAQ.html')

def ug_exam_details(request):
    return render(request, 'home/ug_exam_details.html')


def ug_syllabus(request):
    return render(request, 'home/ug_syllabus.html')


def UGFAQ(request):
    return render(request, 'home/UGFAQ.html')