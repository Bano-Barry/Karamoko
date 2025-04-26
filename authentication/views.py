from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomLoginForm

# Vue personnalisée pour la connexion qui utilise un formulaire personnalisé et redirige les utilisateurs authentifiés
class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'  # Modèle pour la page de connexion
    authentication_form = CustomLoginForm       # Formulaire personnalisé pour l'authentification
    redirect_authenticated_user = True          # Redirige les utilisateurs déjà authentifiés

# Vue personnalisée pour la déconnexion qui redirige vers la page de connexion après la déconnexion
class CustomLogoutView(LogoutView):
    next_page = 'login'  # Page vers laquelle rediriger après la déconnexion

# Vue pour l'enregistrement des utilisateurs
def register(request):
    if request.method == 'POST':  # Si le formulaire est soumis
        form = CustomUserCreationForm(request.POST)  # Associe le formulaire avec les données POST
        if form.is_valid():  # Vérifie si le formulaire est valide
            user = form.save()  # Enregistre le nouvel utilisateur
            login(request, user)  # Connecte le nouvel utilisateur
            return redirect('dashboard_home')  # Redirige vers le tableau de bord après l'enregistrement
    else:
        form = CustomUserCreationForm()  # Crée un formulaire vide pour les requêtes GET
    return render(request, 'authentication/register.html', {'form': form})  # Affiche la page d'enregistrement avec le formulaire
