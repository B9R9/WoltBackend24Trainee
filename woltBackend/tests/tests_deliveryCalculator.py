from django.test import TestCase
from datetime import datetime
from deliveryCalculators.deliveryFeeCalculator import DeliveryFeeCalculator
from deliveryCalculators.utils import DeliveryForm
import logging

logger = logging.getLogger('log')

class DeliveryFeeCalculatorTest(TestCase):
    logger.info('Testing the DeliveryFeeCalculator class.')
    def test_calculate_cost_regular_case(self):
        """Test the calculate_cost method with regular input values."""
        data = {
            'cart_value': 790,
            'delivery_distance': 2245,
            'number_of_items': 4,
            'time': '2024-01-15T16:00:00Z',
        }
        calculator = DeliveryFeeCalculator()
        cost = calculator.calculate_cost(data)
        self.assertEqual(cost, 710, f"Expected cost: 710, got {cost}")

    def test_calculate_cost_minimum_values(self):
        """Test the calculate_cost method with minimum input values."""
        data = {
            'cart_value': 1,
            'delivery_distance': 1,
            'number_of_items': 1,
            'time': '2024-01-15T14:00:00Z',
        }
        calculator = DeliveryFeeCalculator()
        cost = calculator.calculate_cost(data)
        self.assertEqual(cost, (1000 - 1) + 200, f"Expected cost: 1199, got {cost}")

    def test_calculate_cost_maximum_values(self):
        """Test the calculate_cost method with maximum input values."""
        data = {
            'cart_value': 10000,
            'delivery_distance': 10000,
            'number_of_items': 20,
            'time': '2024-01-15T16:00:00Z',
        }
        calculator = DeliveryFeeCalculator()
        cost = calculator.calculate_cost(data)
        self.assertEqual(cost, 1500, f"Expected cost: 1500 got {cost}")  # Due to the maximum limit

    def test_calculate_cost_rush_hour_surcharge(self):
        """Test the calculate_cost method during rush hour to check the surcharge."""
        data = {
            'cart_value': 800,
            'delivery_distance': 1200,
            'number_of_items': 5,
            'time': '2024-01-19T17:00:00Z',
        }
        calculator = DeliveryFeeCalculator()
        cost = calculator.calculate_cost(data)
        expected_cost = (1000 - 800) + (200 + 100) + ((5 - 4) * 50)
        expected_cost_with_surcharge = (expected_cost * 120) / 100
        self.assertEqual(cost, expected_cost_with_surcharge, f"Expected cost: {expected_cost_with_surcharge}, got {cost}")

    def test_calculate_cost_maximum_delivery_fee(self):
        """Test the calculate_cost method with a total cost exceeding the maximum limit."""
        data = {
            'cart_value': 8000,
            'delivery_distance': 8000,
            'number_of_items': 15,
            'time': '2024-01-15T16:00:00Z',
        }
        calculator = DeliveryFeeCalculator()
        cost = calculator.calculate_cost(data)
        self.assertEqual(cost, 1500, f"Expected cost: 1500 got {cost}")  # Due to the maximum limit

        logger.info('End of DeliveryFeeCalculator class tests.')


class DeliveryFormTest(TestCase):
    logger.info('Testing the DeliveryForm class.')
    def test_valid_data(self):
        """Test the DeliveryForm with valid input data."""
        data = {
            'cart_value': 800,
            'delivery_distance': 1200,
            'number_of_items': 5,
            'time': '2024-01-15T16:00:00Z',
        }
        form = DeliveryForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_fields(self):
        """Test the DeliveryForm with missing fields."""
        data = {
            'cart_value': 800,
            'delivery_distance': 1200,
            'time': '2024-01-15T16:00:00Z',
        }
        form = DeliveryForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_items', form.errors)
        self.assertIn('This field is required.', form.errors['number_of_items'])

    def test_invalid_time_format(self):
        """Test the DeliveryForm with an invalid time format."""
        data = {
            'cart_value': 800,
            'delivery_distance': 1200,
            'number_of_items': 5,
            'time': 'invalid_format',
        }
        form = DeliveryForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors)
        self.assertIn('Invalid time format', form.errors['time'])

    def test_negative_cart_value(self):
        """Test the DeliveryForm with a negative value for cart_value."""
        data = {
            'cart_value': -500,
            'delivery_distance': 1200,
            'number_of_items': 5,
            'time': '2024-01-15T16:00:00Z',
        }
        form = DeliveryForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('cart_value', form.errors)
        self.assertTrue('must be positive' in form.errors['cart_value'][0])

    def test_non_integer_delivery_distance(self):
        """Test the DeliveryForm with a non-integer value for delivery_distance."""
        data = {
            'cart_value': 800,
            'delivery_distance': 1200.5,
            'number_of_items': 5,
            'time': '2024-01-15T16:00:00Z',
        }
        form = DeliveryForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('delivery_distance', form.errors)
        self.assertIn('Enter a whole number.', form.errors['delivery_distance'][0])

    logger.info('End of DeliveryForm class tests.')
