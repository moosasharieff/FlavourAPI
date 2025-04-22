from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Flavour

from .serializers import FlavourDetailSerializer, FlavourSerializer


class FlavourViewSet(viewsets.ModelViewSet):
    """View for managing Flavour API."""

    serializer_class = FlavourSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Flavour.objects.all()

    def get_queryset(self):
        """Return flavour query only for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Overrides the above 'serializer_class' and returns serializer class depending on list or detail request."""
        if self.action == "list":
            return FlavourSerializer
        return FlavourDetailSerializer

    def perform_create(self, serializer):
        """Override default create method for creating Flavour through API."""
        serializer.save(user = self.request.user)
