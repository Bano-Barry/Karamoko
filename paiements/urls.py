from django.urls import path
from . import views

urlpatterns = [
    # URLs pour MethodePaiement
    path('methodes-paiements/', views.MethodePaiementListView.as_view(), name='methodepaiement_list'),
    path('methodes-paiements/create/', views.MethodePaiementCreateView.as_view(), name='methodepaiement_create'),
    path('methodes-paiements/<int:pk>/update/', views.MethodePaiementUpdateView.as_view(), name='methodepaiement_update'),
    path('methodes-paiements/<int:pk>/delete/', views.MethodePaiementDeleteView.as_view(), name='methodepaiement_delete'),

    # # URLs pour PlanTarifaire
    # path('plans-tarifaires/', views.PlanTarifaireListView.as_view(), name='plantarifaire_list'),
    # path('plans-tarifaires/create/', views.PlanTarifaireCreateView.as_view(), name='plantarifaire_create'),
    # path('plans-tarifaires/<int:pk>/update/', views.PlanTarifaireUpdateView.as_view(), name='plantarifaire_update'),
    # path('plans-tarifaires/<int:pk>/delete/', views.PlanTarifaireDeleteView.as_view(), name='plantarifaire_delete'),

    # # URLs pour Paiement
    # path('paiements/', views.PaiementListView.as_view(), name='paiement_list'),
    # path('paiements/create/', views.PaiementCreateView.as_view(), name='paiement_create'),
    # path('paiements/<int:pk>/update/', views.PaiementUpdateView.as_view(), name='paiement_update'),
    # path('paiements/<int:pk>/delete/', views.PaiementDeleteView.as_view(), name='paiement_delete'),
]