from django.urls import path
from .views import PredictAPIView, PredictionListAPIView
from .views import PredictAPIView, PredictionListAPIView, get_addresses
from django.views.generic import TemplateView

urlpatterns = [
    path('api/predict/', PredictAPIView.as_view(), name='api_predict'),
    path('api/predictions/', PredictionListAPIView.as_view(), name='api_predictions'),
    path('api/addresses/', get_addresses, name='api_addresses'),
    path('', TemplateView.as_view(template_name='housing/index.html'), name='index'),
]