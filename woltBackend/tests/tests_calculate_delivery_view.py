from django.test import TestCase
from django.urls import reverse
import json
import logging

logger = logging.getLogger('log')

class CalculateDeliveryTestCase(TestCase):
    """Test the calculate_delivery view."""
    logger.info('Testing the calculate_delivery view.')
    def setUp(self):
        # Set up the URL for the calculate_delivery view
        self.url = reverse('calculate_delivery')

    def test_successful_calculation(self):
        """Test the successful calculation of delivery fee."""
        data = {
            'cart_value': 1000,
            'delivery_distance': 1500,
            'number_of_items': 3,
            'time': '2024-01-15T13:00:00Z',
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('delivery_fee', json_response)
        self.assertIsInstance(json_response['delivery_fee'], (int, float))

    def test_missing_fields(self):
        """Test handling missing fields in the input data."""
        data = {
            'cart_value': 1000,
            'delivery_distance': 1500,
            'time': '2024-01-15T13:00:00Z',
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        json_response = response.json()
        self.assertIn('error', json_response)
        self.assertIn('number_of_items', json_response['error'])

    def test_invalid_data(self):
        """Test handling invalid data types in the input."""
        data = {
            'cart_value': 'invalid',
            'delivery_distance': 'invalid',
            'number_of_items': 'invalid',
            'time': 'invalid',
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        json_response = response.json()
        self.assertIn('error', json_response)
        self.assertIsInstance(json_response['error'], dict)

    def test_negative_cart_value(self):
        """Test handling a negative value for cart_value."""
        data = {
            'cart_value': -500,
            'delivery_distance': 1500,
            'number_of_items': 3,
            'time': '2024-01-15T13:00:00Z',
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        json_response = response.json()
        self.assertIn('error', json_response)
        self.assertIn('cart_value', json_response['error'])

    logger.info('Finished testing the calculate_delivery view.')
