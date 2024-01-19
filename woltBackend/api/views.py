from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# Create your views here.

@csrf_exempt
@require_POST
def calculate(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		result = data['a'] + data['b']
		return JsonResponse({'result': result})
	except (KeyError, TypeError) as e:
		return JsonResponse({'error': 'Invalid input data'}, status=400)

