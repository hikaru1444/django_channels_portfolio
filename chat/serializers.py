from chat.models import Shop
from rest_framework import serializers


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
