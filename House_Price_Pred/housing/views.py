from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import PredictionRequestSerializer
from .models import PredictionRequest
from . import utils
from rest_framework.decorators import api_view
import pandas as pd
import os

class PredictAPIView(APIView):
    """
    POST JSON:
    {
      "area": 120.5,
      "room": 3,
      "parking": 1,
      "warehouse": 0,
      "elevator": 1,
      "address": "DistrictName"
    }
    """
    def post(self, request):
        data = request.data
        # Basic validation (serializer will help too)
        serializer = PredictionRequestSerializer(data=data)
        # allow writing input fields only
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data
        try:
            pred_log, pred_usd = utils.predict_price(
                area=validated['area'],
                room=validated['room'],
                parking=validated['parking'],
                warehouse=validated['warehouse'],
                elevator=validated['elevator'],
                address=validated['address']
            )
        except FileNotFoundError as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'detail': f'Prediction failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save record
        instance = PredictionRequest.objects.create(
            area=validated['area'],
            room=validated['room'],
            parking=validated['parking'],
            warehouse=validated['warehouse'],
            elevator=validated['elevator'],
            address=validated['address'],
            predicted_price_log=pred_log,
            predicted_price_usd=pred_usd
        )
        out_ser = PredictionRequestSerializer(instance)
        return Response(out_ser.data, status=status.HTTP_201_CREATED)

class PredictionListAPIView(generics.ListAPIView):
    queryset = PredictionRequest.objects.order_by('-created_at')[:200]
    serializer_class = PredictionRequestSerializer

@api_view(['GET'])
def get_addresses(request):
    csv_path = os.path.join(os.path.dirname(__file__), 'housePrice.csv')
    df = pd.read_csv(csv_path)
    addresses = sorted(df['Address'].dropna().unique().tolist())
    return Response(addresses)  