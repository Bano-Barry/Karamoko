from django.urls import path
from . import views

urlpatterns = [
    path('', views.souscripteur_list, name='souscripteur_list'),
    path('create/', views.create_souscripteur, name='create_souscripteur'),
    path('<int:id>/', views.detail_souscripteur, name='detail_souscripteur'),
    path('<int:id>/update/', views.update_souscripteur, name='update_souscripteur'),
    path('<int:id>/delete/', views.delete_souscripteur, name='delete_souscripteur'),
]