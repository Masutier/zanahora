from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('reactivate_user/', reactivateUser, name='reactivate_user'),

    path('users/user/', userPage, name='user_page'),
    path('users/user_update', userUpdate, name='user_update'),
    path('users/delete_user/<str:pk>/', deleteUser, name="delete_user"),

    path('password/reset_password/',
     auth_views.PasswordResetView.as_view(template_name='users/password/password_reset.html'),
     name='reset_password' ),
    path('password/reset_password_sent/',
     auth_views.PasswordResetDoneView.as_view(template_name='users/password/password_reset_sent.html'),
     name='password_reset_done'),
    path('password/reset/<uidb64>/<token>',
     auth_views.PasswordResetConfirmView.as_view(template_name='users/password/password_reset_form.html'),
     name='password_reset_confirm'),
    path('password/reset_password_complete',
     auth_views.PasswordResetCompleteView.as_view(template_name='users/password/password_reset_done.html'),
     name='password_reset_complete'),

]