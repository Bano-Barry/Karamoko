from django.urls import path

from repetiteurs.views import repetiteur_public_detail

from . import views

urlpatterns = [
    path('karamoko/', views.home, name='home'),
    path('karamoko/encadreurs/', views.encadreurs, name='encadreurs'),
    path('karamoko/about/', views.about, name='about'),
    path('karamoko/guide_parent/', views.guide_parent, name='guide_parent'),
    path('karamoko/guide_repetiteur/', views.guide_repetiteur, name='guide_repetiteur'),
    path('dashboard/niveaux/', views.NiveauListView.as_view(), name='niveau_list'),
    path('dashboard/niveaux/create/', views.NiveauCreateView.as_view(), name='niveau_create'),
    path('dashboard/niveaux/<int:pk>/update/', views.NiveauUpdateView.as_view(), name='niveau_update'),
    path('dashboard/niveaux/<int:pk>/delete/', views.NiveauDeleteView.as_view(), name='niveau_delete'),
    
    # urls publics pour les répétiteurs
    path('repetiteur/<int:id>/', repetiteur_public_detail, name='repetiteur_public_detail'),

    path('karamoko/test-404/', views.trigger_404, name='test_404'),
    
    path('ajax/matieres-par-niveau/<int:niveau_id>/', 
         views.ajax_matieres_par_niveau, 
         name='ajax_matieres_par_niveau'),
    
    # Offres par niveau avec matières sélectionnées
    path('ajax/offres-par-niveau/<int:niveau_id>/', 
         views.ajax_offres_par_niveau, 
         name='ajax_offres_par_niveau'),
    
    # Debug (optionnel - pour développement)
    path('ajax/debug-niveau/<int:niveau_id>/', 
         views.ajax_debug_niveau, 
         name='ajax_debug_niveau'),
]