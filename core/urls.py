from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('encadreurs/', views.encadreurs, name='encadreurs'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    # path('login/', views.login_view, name='login'),
    # path('register/', views.register_view, name='register'),
    path('niveaux/', views.NiveauListView.as_view(), name='niveau_list'),
    path('niveaux/create/', views.NiveauCreateView.as_view(), name='niveau_create'),
    path('niveaux/<int:pk>/update/', views.NiveauUpdateView.as_view(), name='niveau_update'),
    path('niveaux/<int:pk>/delete/', views.NiveauDeleteView.as_view(), name='niveau_delete'),
]