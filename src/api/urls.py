from django.urls import path
from .views import *

urlpatterns = [
    path('resorts/', GetResortsList.as_view()),
    path('resort/<int:id>/', GetResorts.as_view()),
    path('resortPrices/<int:id>/', GetResortPrices.as_view())
]