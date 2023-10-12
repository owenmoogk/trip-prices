from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Resort(models.Model):
  name = models.CharField(max_length=255)

class PriceDataPoint(models.Model):
  resort = models.ForeignKey(Resort, on_delete=models.CASCADE)
  price = models.FloatField()
  dateCollected = models.DateField()
  tripStartDate = models.DateField()
  tripEndDate = models.DateField()

class ResortUserLike(models.Model):
  resort = models.ForeignKey(Resort, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)