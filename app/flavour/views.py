from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Flavour

from .serializers import FlavourSerializer


class FlavourViewSet(viewsets.ModelViewSet):
    """View for managing Flavour API."""

    serializer_class = FlavourSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Flavour.objects.all()

    def get_queryset(self):
        """Return flavour query only for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")
