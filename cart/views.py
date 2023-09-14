from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from user.utils import user_verify
from .models import Cart
from .serializers import CartSerializer


class CartAPI(viewsets.ViewSet):
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={"book": openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 "total_quantity": openapi.Schema(
                                                                     type=openapi.TYPE_INTEGER)},
                                                     required=["book", "total_quantity"]),
                         operation_summary="Cart Creation")
    @user_verify
    def create(self, request):
        try:
            serializer = CartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Cart Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @user_verify
    def list(self, request):
        try:
            cart = Cart.objects.filter(user=request.data.get("user"))
            serializer = CartSerializer(cart, many=True)
            return Response({"message": "Cart Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={"id": openapi.Schema(type=openapi.TYPE_INTEGER)},
                                                     required=["id", "user"]),
                         operation_summary="Cart Deletion")
    @user_verify
    def destroy(self, request):
        try:
            cart = Cart.objects.filter(id=request.data.get("id"), user=request.data.get("user"))
            cart.delete()
            return Response({"message": "Cart Deleted", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class IsOrdered(viewsets.ViewSet):
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={"id": openapi.Schema(type=openapi.TYPE_INTEGER)},
                                                     required=["id", "user"]), operation_summary="Order")
    @user_verify
    def create(self, request):
        try:
            cart = Cart.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            cart.is_ordered = True
            cart.save()
            return Response({"message": "Order Success", "status": 201, "data": cart.is_ordered},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @user_verify
    def list(self, request):
        try:
            cart = Cart.objects.filter(user=request.data.get("user"), is_ordered=True)
            serializer = CartSerializer(cart, many=True)
            return Response({"message": "Order Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={"id": openapi.Schema(type=openapi.TYPE_INTEGER)},
                                                     required=["id", "user"]), operation_summary="Cancel Order")
    @user_verify
    def destroy(self, request):
        try:
            cart = Cart.objects.filter(id=request.data.get("id"), user=request.data.get("user"))
            cart.delete()
            return Response({"message": "Order Canceled", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
