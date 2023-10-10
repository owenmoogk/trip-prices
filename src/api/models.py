from django.db import models

# Create your models here.

class Resort(models.Model):
  name = models.CharField(max_length=255)

class PriceDataPoint(models.Model):
  resort = models.ForeignKey(Resort, on_delete=models.CASCADE)
  price = models.FloatField()
  date = models.DateField()