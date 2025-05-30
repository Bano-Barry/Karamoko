from django.urls import path
from . import views

urlpatterns = [
    path('souscriptions/', views.SouscriptionListView.as_view(), name='souscription_list'),
    path('souscriptions/create/', views.SouscriptionCreateView.as_view(), name='souscription_create'),
    path('souscriptions/<int:pk>/update/', views.SouscriptionUpdateView.as_view(), name='souscription_update'),
    path('souscriptions/<int:pk>/delete/', views.SouscriptionDeleteView.as_view(), name='souscription_delete'),
    path('souscriptions/<int:pk>/', views.SouscriptionDetailView.as_view(), name='souscription_detail'),

    path('souscriptions/affecter/<int:demande_id>/', views.affecter_demande_souscription, name='affecter_demande_souscription'),
    path('souscriptions/demandes-souscriptions/', views.liste_demandes_souscription, name='liste_demandes_souscription'), 
    path('souscriptions/demandes-souscriptions/<int:demande_id>/', views.demande_souscription_detail, name='demande_souscription_detail'),
]