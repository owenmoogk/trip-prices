from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.db.models import F, Q, Count, Exists, OuterRef

class GetResorts(APIView):
  
  permission_classes = (permissions.AllowAny,)

  def get(self, request, id):

    try:
      resort = Resort.objects.get(id=id)
      return Response(ResortSerializer(resort).data)
    except:
      return Response(status=status.HTTP_404_NOT_FOUND)

class GetResortsList(APIView):

  def get(self, request):

    try:
      resorts = Resort.objects.annotate(liked=Exists(ResortUserLike.objects.filter(user = request.user, resort = OuterRef("pk"))))
      return Response(ResortLikedSerializer(resorts, many=True).data)

    except Exception as e:
      print(e)
      return Response(status=status.HTTP_404_NOT_FOUND)
    

class GetResortPrices(APIView):

  permission_classes = (permissions.AllowAny,)

  def get(self, request, id):

    try:
      return Response(PriceDataPointSerializer(getResortPrices(id), many=True).data)
    except Exception as e:
      print(e)
      return Response(status=status.HTTP_404_NOT_FOUND)

class FavoriteResort(APIView):

  def post(self, request):

    try:

      if (request.data["dislike"]):
        userLike = ResortUserLike.objects.filter(user = request.user, resort = Resort.objects.get(id = request.data["id"]))
        userLike.delete()
      else:
        userLike = ResortUserLike(resort = Resort.objects.get(id = request.data["id"]), user = request.user)
        userLike.save()
      return Response(status=status.HTTP_200_OK)
    
    except Exception as e:
      print(e)
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class FavoriteResortData(APIView):

  def get(self, request):

    likedObjects = ResortUserLike.objects.select_related("resort").filter(user = request.user)
    likedResorts = [likedObject.resort for likedObject in likedObjects]

    resortPrices = {}
    for resort in likedResorts:
      resortPrices[resort.id] = PriceDataPointSerializer(getResortPrices(resort.id), many=True).data

    return Response(resortPrices, status=status.HTTP_200_OK)


# helper function
def getResortPrices(id):
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

  selectedPrices.sort(key=lambda x:x.date)
  return selectedPrices