#api/urls.py

from django.urls import path
from .views import calculate_delivery

urlpatterns = [
	path('deliveryCalculator/', calculate_delivery, name='calculate_delivery'),
]