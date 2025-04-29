from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from repetiteurs.forms import RepetiteurProfileForm
from repetiteurs.models import Repetiteur
from souscripteurs.forms import SouscripteurProfileForm
from souscripteurs.models import Souscripteur
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
            # Vérifie le rôle choisi et crée l'enregistrement correspondant
            if user.role == 'repetiteur':
                repetiteur = Repetiteur.objects.create(user=user)  # Crée un répétiteur lié à l'utilisateur
                print(f"Répétiteur créé : {repetiteur}")
            elif user.role == 'parent':
                souscripteur = Souscripteur.objects.create(user=user)  # Crée un souscripteur lié à l'utilisateur
                print(f"Souscripteur créé : {souscripteur}")
            else:  # Si le rôle n'est pas reconnu, on ne fait rien
                pass
            login(request, user)  # Connecte le nouvel utilisateur
            return redirect('dashboard_home')  # Redirige vers le tableau de bord après l'enregistrement
    else:
        form = CustomUserCreationForm()  # Crée un formulaire vide pour les requêtes GET
    return render(request, 'authentication/register.html', {'form': form})  # Affiche la page d'enregistrement avec le formulaire


@login_required
def complete_repetiteur_profile(request):
    repetiteur = get_object_or_404(Repetiteur, user=request.user)
    if request.method == 'POST':
        form = RepetiteurProfileForm(request.POST, request.FILES, instance=repetiteur)
        if form.is_valid():
            form.save()
            return redirect('dashboard_home')  # Redirige vers le tableau de bord après la mise à jour
    else:
        form = RepetiteurProfileForm(instance=repetiteur)
    return render(request, 'repetiteurs/complete_profile.html', {'form': form})

@login_required
def complete_souscripteur_profile(request):
    souscripteur = get_object_or_404(Souscripteur, user=request.user)
    if request.method == 'POST':
        form = SouscripteurProfileForm(request.POST, request.FILES, instance=souscripteur)
        if form.is_valid():
            form.save()
            return redirect('dashboard_home')  # Redirige vers le tableau de bord après la mise à jour
    else:
        form = SouscripteurProfileForm(instance=souscripteur)
    return render(request, 'souscripteurs/complete_profile.html', {'form': form})