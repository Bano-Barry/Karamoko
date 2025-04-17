from django.urls import path
from . import views


urlpatterns = [
    path('', views.SouscripteurListView.as_view(), name='souscripteur_list'),
    path('<int:pk>/', views.SouscripteurDetailView.as_view(), name='souscripteur_detail'), 
    path('create/', views.SouscripteurCreateView.as_view(), name='souscripteur_create'),
    path('<int:pk>/update/', views.SouscripteurUpdateView.as_view(), name='souscripteur_update'),
    path('<int:pk>/delete/', views.SouscripteurDeleteView.as_view(), name='souscripteur_delete'),
]