from django.urls import path
from cart import views

urlpatterns = [
    path("api/cart", views.CartAPI.as_view({'post': 'create', 'get': 'list', 'delete': 'destroy'}), name="cart"),
    path("api/is_ordered", views.IsOrdered.as_view({'post': 'create', 'get': 'list', 'delete': 'destroy'}),
         name="order")
]
