from django.urls import path

from . import views

urlpatterns = [
    path('register_user', views.register_user),
    path('login_user', views.login_user),
    path('remove_user', views.remove_user),
]
