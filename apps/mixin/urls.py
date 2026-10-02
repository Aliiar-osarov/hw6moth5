from django.urls import path, include
from .views import HumanViewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('human', HumanViewsets)

urlpatterns = [
    path('', include(router.urls))
    # path('', MixinView.as_view(), name='mixin-list'),
    # path('<int:pk>/', MixinDetailView.as_view(), name='mixin-detail')
]

