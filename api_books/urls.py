from django.urls import path

from .viewset.user_views import views
from .viewset.books_views import books_views

urlpatterns = [
    path('register_user', views.register_user),
    path('login_user', views.login_user),
    path('remove_user', views.remove_user),
    path('all_books', books_views.get_books),
    path('create_book', books_views.create_books),
]
