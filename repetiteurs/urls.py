from django.urls import path
from . import views

urlpatterns = [
    # URLs pour les compétences
    path('competences/', views.CompetenceListView.as_view(), name='competence_list'),
    path('competences/create/', views.CompetenceCreateView.as_view(), name='competence_create'),
    path('competences/<int:pk>/update/', views.CompetenceUpdateView.as_view(), name='competence_update'),
    path('competences/<int:pk>/delete/', views.CompetenceDeleteView.as_view(), name='competence_delete'),
    # URLs pour les répétiteurs
    path('repetiteurs/', views.repetiteur_list, name='repetiteur_list'),
    path('repetiteurs/create/', views.repetiteur_create, name='repetiteur_create'),
    path('repetiteurs/<int:id>/', views.repetiteur_detail, name='repetiteur_detail'),
    path('repetiteurs/<int:pk>/edit/', views.repetiteur_update, name='repetiteur_update'),
    path('repetiteurs/<int:pk>/delete/', views.repetiteur_delete, name='repetiteur_delete'),
    # URLs pour les cours
    path('cours/', views.CoursListView.as_view(), name='cours_list'),
    path('cours/create/', views.CoursCreateView.as_view(), name='cours_create'),
    path('cours/<int:pk>/update/', views.CoursUpdateView.as_view(), name='cours_update'),
    path('cours/<int:pk>/delete/', views.CoursDeleteView.as_view(), name='cours_delete'),
    # path('cours/<int:pk>/detail/', views.CoursDetailView.as_view(), name='cours_detail'),
    path('encadreurs/', views.vitrine_repetiteur_list, name='vitrine_repetiteur_list'),
    
    # urls pour les souscriptions 
    path('souscription/create/<int:repetiteur_id>/', views.souscription_create, name='souscription_create'),
    # path('souscription/<int:repetiteur_id>/detail/', views.souscription_detail, name='souscription_detail'),
    # path('souscription/<int:repetiteur_id>/update/', views.souscription_update, name='souscription_update'),
    # path('souscription/<int:repetiteur_id>/delete/', views.souscription_delete, name='souscription_delete'),
]