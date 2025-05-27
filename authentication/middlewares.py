from django.shortcuts import redirect
from django.urls import reverse

class CheckRepetiteurValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Laisser passer les fichiers statiques et médias
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        user = request.user

        if user.is_authenticated and getattr(user, 'role', None) == 'repetiteur':
            repetiteur = getattr(user, 'repetiteur', None)

            # Étape 1 : le profil de répétiteur n’a même pas été complété
            if not repetiteur or not repetiteur.is_profile_complete():
                allowed_paths = [
                    reverse('complete_repetiteur_profile'),
                    reverse('logout'),
                    reverse('dashboard_home'),  
                    reverse('home'),    
                    reverse('guide_repetiteur'),  # page d'accueil répétiteur
                ]
                if request.path not in allowed_paths:
                    return redirect('dashboard_home')

            # Étape 2 : profil complet mais pas encore validé par l’admin
            elif not user.is_validated:
                allowed_paths = [
                    reverse('logout'),
                    reverse('dashboard_home'),  # affiche le message de profil en attente
                    reverse('home'),
                    reverse('complete_repetiteur_profile'),  # pour modifier le profil
                ]
                if request.path not in allowed_paths:
                    return redirect('dashboard_home')  # ou une vue d’attente si tu préfères

        return self.get_response(request)
