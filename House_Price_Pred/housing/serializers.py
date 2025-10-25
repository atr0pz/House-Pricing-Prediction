from rest_framework import serializers
from .models import District, House


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'avg_price']


class PredictionInputSerializer(serializers.Serializer):
    area = serializers.FloatField()
    rooms = serializers.IntegerField()
    year_built = serializers.IntegerField()
    district = serializers.CharField() # accept district name
    parking = serializers.BooleanField(default=False)
    elevator = serializers.BooleanField(default=False)
    storage = serializers.BooleanField(default=False)


class PredictionOutputSerializer(serializers.Serializer):
    predicted_price = serializers.FloatField()
    message = serializers.CharField()


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'