from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    
    path('task/<str:pk>', views.taskPage, name='task'),
    
    path('create-task/', views.createTask, name='create-task'),
    path('edit-task/<str:pk>', views.editTask, name='edit-task'),
    path('delete-task/<str:pk>', views.deleteTask, name='delete-task'),
    path('complete-task/<str:pk>', views.completeTask, name='complete-task'),
    
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    
]