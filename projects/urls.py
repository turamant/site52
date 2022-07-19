from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('create_project/', views.create_project, name='create_project'),
    path('project_object/<str:pk>/', views.get_project, name="project"),
    path('update_project/<str:pk>/', views.update_project, name='update_project'),
    path('delete_project/<str:pk>/', views.delete_project, name='delete_project'),
    path('tag/<slug:tag_slug>', views.projects_by_tag, name="tag"),
    path('', views.get_projects, name="projects"),
]