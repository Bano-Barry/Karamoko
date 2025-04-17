from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('niveaux/', views.NiveauListView.as_view(), name='niveau_list'),
    path('niveaux/create/', views.NiveauCreateView.as_view(), name='niveau_create'),
    path('niveaux/<int:pk>/update/', views.NiveauUpdateView.as_view(), name='niveau_update'),
    path('niveaux/<int:pk>/delete/', views.NiveauDeleteView.as_view(), name='niveau_delete'),
]