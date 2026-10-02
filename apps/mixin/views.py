from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import mixins, viewsets

from django_filters.rest_framework import DjangoFilterBackend ###
from rest_framework.filters import SearchFilter, OrderingFilter ###

from .models import Mixin, Human
from .serialzers import MixinSerializer, HumanSerializer
from .pagination import HumanPag
# Create your views here.

# class MixinView(mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 GenericAPIView): # 
    
#     queryset = Mixin.objects.all()
#     serializer_class = MixinSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     print('cоздаеттся книга')

    #     self.response = super().create(request, *args, **kwargs)
    #     return self.response 
    
    # def perform_create(self, serializer):
    #     serializer.save()

    # def perform_create(self, serializer):
    #     serializer.save(title=self.request.user)


    
# class MixinDetailView(mixins.RetrieveModelMixin,
#                 mixins.UpdateModelMixin,
#                 mixins.DestroyModelMixin,
#                 GenericAPIView): # 
    
#     queryset = Mixin.objects.all()
#     serializer_class = MixinSerializer

#     def get(self, request, *args, **kwargs): # kwargs = pk
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

class HumanViewsets(viewsets.ModelViewSet):
    queryset = Human.objects.all().order_by('id',)
    serializer_class = HumanSerializer
    
    pagination_class = HumanPag

    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]

    filter_fields = ('title',) 
    search_fields = ('title', 'description')

    ordering = ('title',) # order = 1 

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]


        return [permission() for permission in self.permission_classes]
