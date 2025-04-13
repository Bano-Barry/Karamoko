from django.shortcuts import render

def dashboard_home(request):
    return render(request, 'dashboard/home.html')  # Page d'accueil avec la structure globale

# Create your views here.
