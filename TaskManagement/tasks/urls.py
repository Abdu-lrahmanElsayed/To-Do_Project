from django.urls import path
from . import views

urlpatterns = [
    path('<int:project_id>/tasks/create', views.task_create, name='task-create'),
    path('<int:project_id>/tasks/', views.task_list, name='task-list'),
    path('<int:project_id>/tasks/<int:task_id>/', views.task_details, name='task-details'),
    path('<int:project_id>/tasks/<int:task_id>/update', views.task_update, name='task-update'),
    path('<int:project_id>/tasks/<int:task_id>/delete', views.task_delete, name='task-delete'),
]