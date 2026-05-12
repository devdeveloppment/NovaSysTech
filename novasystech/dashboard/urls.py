from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('login/', views.dashboard_login, name='dashboard_login'),
    path('logout/', views.dashboard_logout, name='dashboard_logout'),
    path('devis/', views.devis_list, name='devis_list'),
    path('devis/<int:pk>/', views.devis_detail, name='devis_detail'),
    path('devis/export/', views.devis_export, name='devis_export'),
    path('devis/<int:pk>/statut/', views.update_statut, name='update_statut'),
    path('messages/', views.messages_list, name='messages_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/<int:pk>/reply/', views.message_reply, name='message_reply'),
    path('services/', views.services_list, name='services_list'),
    path('temoignages/', views.temoignages_list, name='temoignages_list'),
    path('projets/', views.projets_list, name='projets_list'),
    path('articles/', views.articles_list, name='articles_list'),
    path('newsletter/', views.newsletter_list, name='newsletter_list'),
]
