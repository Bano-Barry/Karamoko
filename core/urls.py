from django.urls import path

from repetiteurs.views import repetiteur_public_detail

from . import views

urlpatterns = [
    path('karamoko/', views.home, name='home'),
    path('karamoko/encadreurs/', views.encadreurs, name='encadreurs'),
    path('karamoko/services/', views.services, name='services'),
    path('karamoko/about/', views.about, name='about'),
    path('dashboard/niveaux/', views.NiveauListView.as_view(), name='niveau_list'),
    path('dashboard/niveaux/create/', views.NiveauCreateView.as_view(), name='niveau_create'),
    path('dashboard/niveaux/<int:pk>/update/', views.NiveauUpdateView.as_view(), name='niveau_update'),
    path('dashboard/niveaux/<int:pk>/delete/', views.NiveauDeleteView.as_view(), name='niveau_delete'),
    
    # urls publics pour les répétiteurs
    path('repetiteur/<int:id>/', repetiteur_public_detail, name='repetiteur_public_detail'),

]