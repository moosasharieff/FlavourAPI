"""
# app/flavour/serializers.py
Serializers for recipe APIs.
"""

from rest_framework import serializers

from app.core.models import Flavour


class FlavourSerializer(serializers.ModelSerializers):
    """Serializer for Flavour API."""

    class Meta:
        model = Flavour
        fields = ["id", "title", "description", "price", "time_minutes", "link"]
        ready_only_fields = ["id"]
