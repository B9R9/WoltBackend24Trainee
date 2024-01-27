from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from deliveryCalculators.deliveryFeeCalculator import DeliveryFeeCalculator
from deliveryCalculators.utils import DeliveryForm
from typing import Union, Dict
import logging
import json


logs = logging.getLogger('log') 
calculator = DeliveryFeeCalculator()

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
@csrf_exempt
@require_POST
def calculate_delivery(request: HttpRequest) -> JsonResponse:
	"""
    View to calculate delivery fees based on the input data.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        JsonResponse: JSON response containing the calculated delivery fee or an error message.
    """
	try:
		data = json.loads(request.body.decode('utf-8'))
		logs.info(f"Request : {data}")
		form = DeliveryForm(data)
		if form.is_valid():
			data = form.cleaned_data
			cost = calculator.calculate_cost(data)
			logs.info(f"Response : {cost}")
			return JsonResponse({'delivery_fee': cost})
		else:
			logs.error(f"Form error")
			return JsonResponse({'error': form.errors}, status=400)
	except (KeyError, TypeError) as e:
		logs.error(f"{str(e)}")
		return JsonResponse({'error': 'Invalid input data'}, status=400)
