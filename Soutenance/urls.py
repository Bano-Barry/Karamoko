from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Page d'accueil
    path('dashboard/', include('dashboard.urls')),  # URL pour le dashboard
    path('dashboard/repetiteurs/', include('repetiteurs.urls')),
    path('dashboard/souscripteurs/', include('souscripteurs.urls')),
    path('dashboard/', include('formations.urls')), # URL pour les formations
    path('dashboard/', include('paiements.urls')),  # URL pour les paiements
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
