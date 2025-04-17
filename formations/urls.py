from django.urls import path
from . import views

urlpatterns = [
    path('types-formations/', views.TypeFormationListView.as_view(), name='typeformation_list'),  # Liste des types de formation
    path('types-formations/create/', views.TypeFormationCreateView.as_view(), name='typeformation_create'),  # Création d'un type de formation
    path('types-formations/<int:pk>/update/', views.TypeFormationUpdateView.as_view(), name='typeformation_update'),  # Modification d'un type de formation
    path('types-formations/<int:pk>/delete/', views.TypeFormationDeleteView.as_view(), name='typeformation_delete'),  # Suppression d'un type de formation

    path('formations/', views.FormationListView.as_view(), name='formation_list'),  # Liste des formations
    path('formations/create/', views.FormationCreateView.as_view(), name='formation_create'),  # Création d'une formation
    path('formations/<int:pk>/update/', views.FormationUpdateView.as_view(), name='formation_update'),  # Modification d'une formation
    path('formations/<int:pk>/delete/', views.FormationDeleteView.as_view(), name='formation_delete'),  # Suppression d'une formation
]