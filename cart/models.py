from django.db import models
from django.template.defaultfilters import default
from book.models import Book
from user.models import User


class Cart(models.Model):
    total_quantity = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    is_ordered = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart'


class CartItems(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'cart_items'

