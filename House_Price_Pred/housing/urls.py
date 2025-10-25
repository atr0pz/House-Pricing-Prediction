from django.urls import path
from . import views


urlpatterns = [
path('', views.index, name='index'),
path('api/districts/', views.DistrictListAPIView.as_view(), name='districts'),
path('api/predict/', views.PredictAPIView.as_view(), name='predict'),
]