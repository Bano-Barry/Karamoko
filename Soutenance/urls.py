from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import complete_repetiteur_profile, complete_souscripteur_profile
from core import views

urlpatterns = [
    path('admin/', admin.site.urls), # URL pour l'admin
    path('karamoko/', include('authentication.urls')),  # URL pour l'authentification
    path('', include('core.urls')),  # URL pour le site vitrine et niveaux
    path('dashboard/', include('dashboard.urls')),  # URL pour le dashboard
    path('dashboard/repetiteurs/', include('repetiteurs.urls')),
    path('dashboard/souscripteurs/', include('souscripteurs.urls')),
    path('dashboard/', include('formations.urls')), # URL pour les formations
    path('dashboard/', include('paiements.urls')),  # URL pour les paiements
    path('dashboard/', include('souscriptions.urls')), #URL pour les souscriptions
    path('complete-profile/repetiteur/', complete_repetiteur_profile, name='complete_repetiteur_profile'),
    path('complete-profile/souscripteur/', complete_souscripteur_profile, name='complete_souscripteur_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
