from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *

class GetResorts(APIView):
  
  permission_classes = (permissions.AllowAny,)

  def get(self, request, id):

    try:
      resort = Resort.objects.get(id=id)
      return Response(ResortSerializer(resort).data)
    except:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
class GetResortsList(APIView):
  
  permission_classes = (permissions.AllowAny,)

  def get(self, request):

    try:
      resorts = Resort.objects.all()
      return Response(ResortSerializer(resorts, many=True).data)
    except Exception as e:
      print(e)
      return Response(status=status.HTTP_404_NOT_FOUND)
    

class GetResortPrices(APIView):

  permission_classes = (permissions.AllowAny,)

  def get(self, request, id):

    try:
      prices = PriceDataPoint.objects.filter(resort = Resort.objects.get(id = id))
      
      # limit to only one data point per day
      datesCovered = set()
      selectedPrices = []
      for price in prices:
        if price.date.strftime("%d/%m/%y") in datesCovered:
          continue
        else:
          datesCovered.add(price.date.strftime("%d/%m/%y"))
          selectedPrices.append(price)

      return Response(PriceDataPointSerializer(selectedPrices, many=True).data)
    except Exception as e:
      print(e)
      return Response(status=status.HTTP_404_NOT_FOUND)