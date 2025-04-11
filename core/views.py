from django.shortcuts import render

def home(request):
    return render(request, 'vitrine/home.html')

# Create your views here.
