from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_portfolio, name='view_portfolio'),
    path('register/', views.register, name='register'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/view/', views.view_profile, name='view_profile'),
    path('portfolio/edit/', views.edit_portfolio, name='edit_portfolio'),
    path('project/add/', views.add_project, name='add_project'),
    path('project/edit/<int:project_id>/', views.edit_project, name='edit_project'),
]

