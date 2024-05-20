# Generated by Django 5.0.6 on 2024-05-20 06:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('book_category', models.CharField(max_length=250)),
                ('book_name', models.CharField(max_length=250)),
                ('book_description', models.TextField()),
                ('book_release_year', models.DateField()),
                ('book_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_email', models.EmailField(default='', max_length=254)),
                ('user_password', models.CharField(max_length=250)),
            ],
        ),
    ]