"""
URls mapping for Flavour API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlavourViewSet

router = DefaultRouter()
router.register('flavours', FlavourViewSet)

app_name = 'flavour'

urlpatterns = [
    path('', include(router.urls))
]