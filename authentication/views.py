from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
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

    def form_valid(self, form):
        messages.success(self.request, 'Connexion réussie. Bienvenue !')  # Message de succès
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de la connexion. Veuillez vérifier vos informations.')  # Message d'erreur
        return super().form_invalid(form)

# Vue personnalisée pour la déconnexion qui redirige vers la page de connexion après la déconnexion
class CustomLogoutView(LogoutView):
    next_page = 'home'  # Page vers laquelle rediriger après la déconnexion

# Vue pour l'enregistrement des utilisateurs
def register(request):
    if request.method == 'POST':  # Si le formulaire est soumis
        form = CustomUserCreationForm(request.POST)  # Associe le formulaire avec les données POST
        if form.is_valid():  # Vérifie si le formulaire est valide
            user = form.save()  # Enregistre le nouvel utilisateur
            messages.success(request, 'Votre compte a été créé avec succès !')  # Message de succès
            # Récupère la valeur de cgu_acceptees du formulaire
            cgu_acceptees = form.cleaned_data.get('cgu_acceptees', False)
            # Vérifie le rôle choisi et crée l'enregistrement correspondant
            if user.role == 'repetiteur':
                Repetiteur.objects.create(user=user, cgu_acceptees=cgu_acceptees)  # Crée un répétiteur lié à l'utilisateur
            elif user.role == 'parent':
                Souscripteur.objects.create(user=user)  # Crée un souscripteur lié à l'utilisateur
            else:  # Si le rôle n'est pas reconnu, on ne fait rien
                pass
            return redirect('login')  # Redirige vers la page de connexion après l'enregistrement
        else : 
            messages.error(request, 'Erreur lors de la création de votre compte. Veuillez vérifier vos informations.')
    else:
        form = CustomUserCreationForm()  # Crée un formulaire vide pour les requêtes GET
    return render(request, 'authentication/register.html', {'form': form})  # Affiche la page d'enregistrement avec le formulaire


# @login_required
# def complete_repetiteur_profile(request):
#     repetiteur = get_object_or_404(Repetiteur, user=request.user)
#     if request.method == 'POST':
#         form = RepetiteurProfileForm(request.POST, request.FILES, instance=repetiteur, user_instance=request.user)  # Récupère le formulaire avec les données de l'utilisateur
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Votre profil a été mis à jour avec succès !')  # Message de succès
#             return redirect('complete_repetiteur_profile')  # Redirige vers la page de mise à jour du profil après la soumission
#     else:
#         form = RepetiteurProfileForm(instance=repetiteur, user_instance=request.user)  # Récupère le formulaire avec les données de l'utilisateur
#     return render(request, 'repetiteurs/complete_profile.html', {'form': form, 'repetiteur': repetiteur})  # Affiche le formulaire de mise à jour du profil

@login_required
def complete_repetiteur_profile(request):
    repetiteur = get_object_or_404(Repetiteur, user=request.user)
    
    if request.method == 'POST':
        # La vue gère maintenant la récupération et la liaison des instances
        form = RepetiteurProfileForm(
            request.POST, 
            request.FILES,
            instance=repetiteur
        )
        
        if form.is_valid():
            submit_final = 'submit_final' in request.POST
            
            # Mise à jour des données utilisateur directement dans la vue
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', user.first_name)
            user.last_name = form.cleaned_data.get('last_name', user.last_name)
            user.email = form.cleaned_data.get('email', user.email)
            user.phone = form.cleaned_data.get('phone', user.phone)
            user.save()
            
            # Sauvegarde du repetiteur
            repetiteur_instance = form.save(commit=False)
            if submit_final:
                repetiteur_instance.is_soumis = True
            repetiteur_instance.save()
            
            # Sauvegarde des relations Many-to-Many
            form.save_m2m()
            
            # Messages de feedback
            if submit_final:
                if repetiteur.is_profile_complete():
                    messages.success(request, '✅ Votre profil a été soumis pour validation.')
                else:
                    messages.warning(request, '⚠️ Votre profil est incomplet, la soumission est bloquée.')
            else:
                messages.success(request, '💾 Vos informations ont été mises à jour avec succès !')
            
            return redirect('complete_repetiteur_profile')
    else:
        # Initialisation du formulaire avec les données existantes
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': getattr(request.user, 'phone', ''),
        }
        form = RepetiteurProfileForm(
            instance=repetiteur,
            initial=initial_data
        )
    
    return render(request, 'repetiteurs/complete_profile.html', {
        'form': form,
        'repetiteur': repetiteur
    })

@login_required
def complete_souscripteur_profile(request):
    souscripteur = get_object_or_404(Souscripteur, user=request.user)
    if request.method == 'POST':
        form = SouscripteurProfileForm(request.POST, request.FILES, instance=souscripteur, user_instance=request.user)  # Récupère le formulaire avec les données de l'utilisateur  
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('complete_souscripteur_profile')  # Redirige vers la page de mise à jour du profil après la soumission
    else:
        form = SouscripteurProfileForm(instance=souscripteur, user_instance=request.user)  # Récupère le formulaire avec les données de l'utilisateur
    return render(request, 'souscripteurs/complete_profile.html', {'form': form})