"""
# app/flavour/serializers.py
Serializers for recipe APIs.
"""

from rest_framework import serializers

from core.models import Flavour


class FlavourSerializer(serializers.ModelSerializer):
    """Serializer for Flavour API."""

    class Meta:
        model = Flavour
        fields = ["id", "title", "price", "time_minutes", "link"]
        read_only_fields = ["id"]


class FlavourDetailSerializer(FlavourSerializer):
    """Serializes single flavour details."""

    class Meta(FlavourSerializer.Meta):
        """Inherite attributes from 'cls: FlavourSerializer' to build this class."""

        fields = FlavourSerializer.Meta.fields + ["description"]
