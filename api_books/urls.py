from django.urls import path
from .viewset.user_views.views import API
from .viewset.books_views.books_views import BooksAPI


urlpatterns = [
    path('register_user', API.register_user),
    path('login_user', API.login_user),
    path('remove_user', API.remove_user),
    path('all_books', BooksAPI.get_books),
    path('create_book', BooksAPI.create_books),
    path('delete_book', BooksAPI.delete_book),
]
