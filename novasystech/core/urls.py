from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('a-propos/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('demande-devis/', views.devis, name='devis'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('mentions-legales/', views.mentions_legales, name='mentions'),
]
