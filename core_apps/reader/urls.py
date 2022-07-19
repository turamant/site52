from django.urls import path

from . import views


app_name = 'reader'

urlpatterns = [
    path('download/<str:file_name>/', views.download_file, name='download_file'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='detail'),
    path('python/', views.BookPython.as_view(), name='python'),
    path('best/', views.BookBest.as_view(), name='best'),
    path('create/', views.BookCreateView.as_view(), name='create'),
    path('book/<int:pk>/edit/', views.BookEditView.as_view(), name='edit'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='delete'),
    path('export/',  views.json_data, name='data'),
    path('', views.BookListView.as_view(), name='index'),
]