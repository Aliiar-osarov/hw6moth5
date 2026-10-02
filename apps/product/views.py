from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,  permissions ## .. 

from django.shortcuts import get_object_or_404 ##

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly ## ..

class ProductApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] ## ..

    def get(self, request):
        products = Product.objects.all()

        # фильтр по категории
        category = request.query_params.get('category')
        if category:
            products = products.filter(category=category)

        # фильтр по наличию
        in_have_param = request.query_params.get('in_have')
        if in_have_param is not None:
            is_in_have = in_have_param.lower() in ['true', '1', 'yes']
            products = products.filter(in_have = is_in_have)
        
        serializer = ProductSerializer(products,  many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) ##

    def post(self, request):
            serializer = ProductSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
    
            return Response(serializer.data, status = status.HTTP_201_CREATED)

class PoductDetail(APIView):

    permission_classes = [IsOwnerOrReadOnly] ## ..
    
    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk) # primary key - первичный ключ - id 

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk): 
        product = self.get_object(pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    
    def patch(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        

     