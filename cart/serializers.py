from rest_framework import serializers
from book.models import Book
from .models import Cart, CartItems


class CartSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'total_quantity', 'total_price', 'is_ordered', 'user', 'book']

    def create(self, validated_data):
        cart, created = Cart.objects.get_or_create(user=validated_data.get("user"), is_ordered=False)
        price = validated_data.get("book").price * validated_data.get("total_quantity")
        cart_item = CartItems.objects.filter(book=validated_data.get("book"), cart=cart).first()
        if not cart_item:
            cart_item = CartItems.objects.create(book=validated_data.get("book"), cart=cart)
        else:
            cart.total_quantity -= cart_item.quantity
            cart.total_price -= cart_item.price
        cart_item.price = price
        cart_item.quantity = validated_data.get("total_quantity")
        cart_item.save()
        cart.total_price += price
        cart.total_quantity += validated_data.get("total_quantity")
        cart.save()
        return cart
