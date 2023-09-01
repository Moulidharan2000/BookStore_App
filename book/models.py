from django.db import models


# Create your models here.
# app = book
# attr = name, author, description, price

class Book(models.Model):
    name = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True)

    class Meta:
        db_table = 'books'
