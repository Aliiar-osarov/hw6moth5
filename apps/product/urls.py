from django.urls import path
from .views import ProductApiView, PoductDetail

urlpatterns = [
    path('', ProductApiView.as_view(), name='product-list'),
    path('<int:pk>/', PoductDetail.as_view(), name='product-detail')
]

