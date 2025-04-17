from django.urls import path
from . import views

urlpatterns = [
    path('souscriptions/', views.SouscriptionListView.as_view(), name='souscription_list'),
    path('souscriptions/create/', views.SouscriptionCreateView.as_view(), name='souscription_create'),
    path('souscriptions/<int:pk>/update/', views.SouscriptionUpdateView.as_view(), name='souscription_update'),
    path('souscriptions/<int:pk>/delete/', views.SouscriptionDeleteView.as_view(), name='souscription_delete'),
]