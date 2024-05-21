from django.db import models
import uuid


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_email = models.EmailField(default='')
    user_password = models.CharField(max_length=250)

    def __str__(self):
        return f'Email: {self.user_email}'


class Books(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book_category = models.CharField(max_length=250)
    book_name = models.CharField(max_length=250)
    book_description = models.TextField()
    book_release_year = models.DateField()
    book_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Name : {self.book_name}'
