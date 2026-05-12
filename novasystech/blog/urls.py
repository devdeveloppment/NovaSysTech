from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
]
