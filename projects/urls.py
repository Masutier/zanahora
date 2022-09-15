from django.urls import path, include
from .views import *

urlpatterns = [
    path('projects_all', projectsAll, name="projects_all"),
    path('proj_detail/<int:id>', project_detail, name='proj_detail'),

    path('create_project/', createProject, name="create_project"),
    path('update_project/<str:pk>', updateProject, name="update_project"),
    path('delete_project/<str:pk>', deleteProject, name="delete_project"),

]