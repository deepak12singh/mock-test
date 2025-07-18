from django.shortcuts import render, HttpResponse

# Create your views here.
def contact(request):
    return render(request,'contact/contact.html' )