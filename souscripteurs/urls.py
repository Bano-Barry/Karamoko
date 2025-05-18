from django.urls import path
from . import views


urlpatterns = [
    path('souscripteurs/', views.SouscripteurListView.as_view(), name='souscripteur_list'),
    path('souscripteurs/<int:pk>/', views.SouscripteurDetailView.as_view(), name='souscripteur_detail'), 
    path('souscripteurs/create/', views.SouscripteurCreateView.as_view(), name='souscripteur_create'),
    path('souscripteurs/<int:pk>/update/', views.SouscripteurUpdateView.as_view(), name='souscripteur_update'),
    path('souscripteurs/<int:pk>/delete/', views.SouscripteurDeleteView.as_view(), name='souscripteur_delete'),
]