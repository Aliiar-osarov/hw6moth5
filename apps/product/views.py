from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import ProductFilter


class ProductApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        products = Product.objects.all()

        # Фильтрация
        product_filter = ProductFilter(
            request.query_params,
            queryset=products
        )
        products = product_filter.qs

        # Поиск
        search = request.query_params.get('search')
        if search:
            products = products.filter(
                title__icontains=search
            ) | products.filter(
                description__icontains=search
            )

        # Пагинация
        paginator = PageNumberPagination()
        paginator.page_size = 5

        page = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class PoductDetail(APIView):

    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(
            instance=product,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(
            instance=product,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

     