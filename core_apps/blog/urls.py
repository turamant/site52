from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('post/<slug:category_slug>/<slug:slug>/', views.detail, name='post_detail'),
    path('category/<slug:slug>/', views.category, name='category_detail'),
    path('about/', views.about, name='about'),
    path('', views.frontpage, name='frontpage'),

]