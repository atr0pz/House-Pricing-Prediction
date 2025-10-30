from django.db import models

class PredictionRequest(models.Model):
    area = models.FloatField()
    room = models.IntegerField()
    parking = models.IntegerField()
    warehouse = models.IntegerField()
    elevator = models.IntegerField()
    address = models.CharField(max_length=200)

    predicted_price_log = models.FloatField(null=True, blank=True) 
    predicted_price_usd = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address} - {self.predicted_price_usd:.2f} USD"