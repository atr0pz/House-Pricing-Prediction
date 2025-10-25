import os
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import (DistrictSerializer, PredictionInputSerializer,
PredictionOutputSerializer, HouseSerializer)
from .models import District, House
import joblib
import numpy as np


# helper: load model and encoder once
MODEL_PATH = os.path.join(settings.BASE_DIR, 'models', 'house_price_model.joblib')
ENCODER_PATH = os.path.join(settings.BASE_DIR, 'models', 'district_encoder.joblib')
_model = None
_encoder = None


def load_model_and_encoder():
    global _model, _encoder
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    if _encoder is None:
        _encoder = joblib.load(ENCODER_PATH)
    return _model, _encoder



# index view -> renders template
def index(request):
    return render(request, 'housing/index.html')




class DistrictListAPIView(generics.ListAPIView):
    queryset = District.objects.all().order_by('name')
    serializer_class = DistrictSerializer




class PredictAPIView(APIView):
    def post(self, request):
        serializer = PredictionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        data = serializer.validated_data


        # preprocess
        # prepare district encoding: if district exists in DB use it, else fallback
        model, encoder = load_model_and_encoder()


        district_name = data['district']
        # encoder is assumed to be a LabelEncoder or similar that maps names -> ints
        try:
            district_encoded = encoder.transform([district_name])[0]
        except Exception:
        # fallback: if new district unseen, try to use mean or 0
            district_encoded = -1


        # feature ordering MUST match training
        features = [
            data['area'],
            data['rooms'],
            data['year_built'],
            district_encoded,
            int(data['parking']),
            int(data['elevator']),
            int(data['storage']),
        ]


        X = np.array(features).reshape(1, -1)
        pred = model.predict(X)
        predicted_price = float(pred[0])


        try:
            district_obj, _ = District.objects.get_or_create(name=district_name)
            House.objects.create(
                area=data['area'],
                rooms=data['rooms'],
                year_built=data['year_built'],
                district=district_obj,
                parking=data['parking'],
                elevator=data['elevator'],
                storage=data['storage'],
            )
        except Exception:
            # don't let DB errors break the API
            pass


        out = {
            'predicted_price': predicted_price,
            'message': 'Prediction successful'
        }
        out_ser = PredictionOutputSerializer(out)
        return Response(out_ser.data)