from django.urls import path
from . import views

urlpatterns = [
    path('', views.repetiteur_list, name='repetiteur_list'),
    path('create/', views.repetiteur_create, name='repetiteur_create'),
    path('<int:id>/', views.repetiteur_detail, name='repetiteur_detail'),
    path('<int:id>/update/', views.repetiteur_update, name='repetiteur_update'),
    path('<int:id>/delete/', views.repetiteur_delete, name='repetiteur_delete'),
]