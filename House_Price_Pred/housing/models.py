from django.db import models


class District(models.Model):
    name = models.CharField(max_length=150, unique=True)
    avg_price = models.FloatField(null=True, blank=True) # optional: precomputed mean price


def __str__(self):
    return self.name


class House(models.Model):
    area = models.FloatField()
    rooms = models.IntegerField()
    year_built = models.IntegerField()
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    parking = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    storage = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return f"{self.area} m2 - {self.district}"