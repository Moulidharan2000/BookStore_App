from django.urls import path
from book import views

urlpatterns = [
    path("api/book/", views.BooksAPI.as_view({'post': 'create', 'get': 'list', 'put': 'update', 'delete': 'destroy'}),
         name="books")
]
