from rest_framework import serializers
from .models import PredictionRequest

class PredictionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionRequest
        fields = [
            'id', 'area', 'room', 'parking', 'warehouse', 'elevator', 'address',
            'predicted_price_log', 'predicted_price_usd', 'created_at'
        ]
        read_only_fields = ['predicted_price_log', 'predicted_price_usd', 'created_at']