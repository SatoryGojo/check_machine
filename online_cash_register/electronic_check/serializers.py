from .models import ItemModel
from rest_framework import serializers

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel
        fields = ['id', 'title', 'price']