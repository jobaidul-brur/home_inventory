from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/?message=<str:message>', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit'),
    path('change-password/', views.change_password, name='change_password'),
    path('deactivate/', views.deactivate_account, name='deactivate'),
]
