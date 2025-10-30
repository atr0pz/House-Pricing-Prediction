from django.contrib import admin
from .models import PredictionRequest

@admin.register(PredictionRequest)
class PredictionRequestAdmin(admin.ModelAdmin):
    list_display = ('address', 'predicted_price_usd', 'area', 'room', 'created_at')
    readonly_fields = ('predicted_price_log', 'predicted_price_usd', 'created_at')