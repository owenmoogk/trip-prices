from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.db.models import Exists, OuterRef
from datetime import datetime

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
      return Response(getResortPrices(id))
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
      resortPrices[resort.name] = getAverageResortPrices(resort.id)

    return Response(resortPrices, status=status.HTTP_200_OK)


# helper function
def getAverageResortPrices(id):
  prices = PriceDataPoint.objects.filter(resort = Resort.objects.get(id = id))

  dateIds = {}
  for price in prices:
    if (dateIds.get(price.dateCollected.strftime("%d/%m/%y"))):
      dateIds[price.dateCollected.strftime("%d/%m/%y")].append(price.id)
    else:
      dateIds[price.dateCollected.strftime("%d/%m/%y")] = [price.id]

  resultData = []
  for date in dateIds.keys():
    datePrices = []
    for priceDataPointId in dateIds[date]:
      datePrices.append(prices.get(id = priceDataPointId).price)

    resultData.append({"dateCollected": datetime.strptime(date, "%d/%m/%y").date(), "price" : round(sum(datePrices) / len(datePrices), 0)})

  return resultData


def getResortPrices(id):
  prices = PriceDataPoint.objects.filter(resort = Resort.objects.get(id = id))
      
  tripStartEndDateSet = set()
  tripStartEndDatePairs = []
  priceData = {}

  for price in prices:
    dateRangeIdentifier = price.tripStartDate.strftime("%d/%m/%y")+price.tripEndDate.strftime("%d/%m/%y")
    if (dateRangeIdentifier) in tripStartEndDateSet:
      pass
    else:
      tripStartEndDateSet.add(dateRangeIdentifier)
      tripStartEndDatePairs.append((price.tripStartDate, price.tripEndDate))
      priceData[dateRangeIdentifier] = []
    
    priceData[dateRangeIdentifier].append({"dateCollected": price.dateCollected, "price": price.price})

  resultData = []
  for tripStartEndDatePair in tripStartEndDatePairs:
    resultData.append({
      "startDate": tripStartEndDatePair[0],
      "endDate": tripStartEndDatePair[1],
      "prices": priceData[tripStartEndDatePair[0].strftime("%d/%m/%y")+tripStartEndDatePair[1].strftime("%d/%m/%y")]
    })

  return resultData