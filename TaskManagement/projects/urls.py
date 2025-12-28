from django.urls import path
from . import views

urlpatterns = [
    path('projects/create', views.project_create, name='project-create'),
    path('projects/', views.admin_project_list, name='project-list'),
    path('user/projects/', views.user_project_list, name='project-list-pk'),
    path('projects/<int:pk>/', views.project_details, name='project-details'),
    path('projects/<int:pk>/update/', views.project_update, name='project-update'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project-delete'),
    ]