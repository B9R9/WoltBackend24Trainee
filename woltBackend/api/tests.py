from django.test import TestCase
import json
from django.urls import reverse
from django.http import JsonResponse

# Create your tests here.
class CalculateViewTest(TestCase):

	def test_calculate_view(self):
		data = {'a': 1, 'b': 2}

		response = self.client.post(reverse('calculate'), data=json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['result'], 3)
		self.assertJSONEqual(str(response.content, encoding='utf8'), json.dumps({'result': 3}))
	
	def test_calculate_view_with_invalid_data(self):
		invalid_data = {'invalid': 'data'}

		response = self.client.post(reverse('calculate'), data=json.dumps(invalid_data), content_type='application/json')
		self.assertEqual(response.status_code, 400)

		self.assertIn('error', response.json())
    	# Vérifiez que le message d'erreur ne doit pas être une chaîne spécifique
		self.assertIsInstance(response.json()['error'], str)

    	# Vous pouvez également vérifier si le message d'erreur contient une partie spécifique
		self.assertIn('Invalid input data', response.json()['error'])
