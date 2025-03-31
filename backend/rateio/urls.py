from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import UsinaViewSet, UnidadeConsumidoraViewSet, RateioViewSet

router = DefaultRouter()
router.register(r'usinas', UsinaViewSet)
router.register(r'unidades-consumidoras', UnidadeConsumidoraViewSet)
router.register(r'rateios', RateioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]