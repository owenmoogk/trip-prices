# import serializer from rest_framework
from rest_framework import serializers
from .models import *

# create a serializer
class ResortSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	name = serializers.CharField(max_length = 255)

class PriceDataPointSerializer(serializers.Serializer):
	resort = ResortSerializer()
	price = serializers.FloatField()
	date = serializers.DateField()