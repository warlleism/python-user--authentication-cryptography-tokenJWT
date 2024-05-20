from django.contrib import admin
from .models import Books, User

admin.site.register(User)
admin.site.register(Books)