from rest_framework import viewsets, status
from user.utils import user_verify, super_user
from .serializers import BookSerializer
from rest_framework.response import Response
from .models import Book
from .utils import RedisBooks
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class BooksAPI(viewsets.ViewSet):
    @swagger_auto_schema(request_body=BookSerializer, operation_summary="Book Creation")
    @super_user
    def create(self, request):
        try:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # RedisBooks.save(request.data.get("id"), serializer.data)
            return Response({"message": "Book Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @user_verify
    def list(self, request):
        try:
            book = Book.objects.all()
            serializer = BookSerializer(book, many=True)
            return Response({"message": "Notes Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=BookSerializer, operation_summary="Book Updation")
    @super_user
    def update(self, request):
        try:
            book = Book.objects.filter(id=request.data.get("id"))
            if not book.exists():
                raise Exception("Book Not Found")
            book = book.first()
            serializer = BookSerializer(book, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # RedisBooks.save(request.data.get("user"), serializer.data)
            return Response({"message": "Book Updated", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={"id": openapi.Schema(type=openapi.TYPE_INTEGER)},
                                                     required=["id"]),
                         operation_summary="Book Deletion")
    @super_user
    def destroy(self, request):
        try:
            book = Book.objects.get(id=request.data.get("id"))
            book.delete()
            # RedisBooks.delete(request.data.get("user"), request.data.get("id"))
            return Response({"message": "Book Deleted", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
