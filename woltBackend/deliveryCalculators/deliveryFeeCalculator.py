import logging
import math
from datetime import datetime, time

logger = logging.getLogger('log')

class DeliveryFeeCalculator:
    """Calculates the delivery fee based on various factors."""

    MIN_CART_VALUE = 1000
    MIN_DISTANCE_DELIVERY = 1000
    DISTANCE_THRESHOLD = 500
    MIN_DISTANCE_DELIVERY_FEE = 200
    COST_SURCHARGE_ITEM = 50
    SURCHARGE_ITEM_THRESHOLD = 4
    COST_BULK_FEE = 120
    BULK_FEE_THRESHOLD = 12
    RUSH_HOUR_START = 15
    RUSH_HOUR_END = 19
    RUSH_HOUR_DAY = "Friday"
    SURCHARGE_RUSH_HOUR = 120
    MAX_DELIVERY_FEE = 1500

    def calculate_cost(self, data):
        """Calculates the total delivery cost based on input data.

        Args:
            data (dict): Input data including cart value, delivery distance, number of items, and delivery time.

        Returns:
            int: Total delivery cost.

        Raises:
            Exception: If any error occurs during the calculation.
        """
        try:
			#Calculte individual costs
            surcharge = self.calculate_surcharge(data['cart_value'])
            delivery_fee_distance = self.calculate_delivery_fee_distance(data['delivery_distance'])
            surcharge_items = self.calculate_surcharge_items(data['number_of_items'])
            rush_hour = self.calculate_time(data['time'])

			#Calculate total cost
            total_cost = surcharge + delivery_fee_distance + surcharge_items
            
			#Apply rush hour surcharge if applicable
            if rush_hour:
                total_cost = (total_cost * self.SURCHARGE_RUSH_HOUR) / 100

			#Apply maximum delivery fee
            if total_cost > self.MAX_DELIVERY_FEE:
                return self.MAX_DELIVERY_FEE

            return total_cost

        except Exception as e:
            logger.error(f"{str(e)}")
            raise

    def calculate_surcharge(self, cart_value):
        """Calculates the surcharge based on the cart value."""
        try:
            if cart_value < self.MIN_CART_VALUE:
                return self.MIN_CART_VALUE - cart_value
            return 0
        except Exception as e:
            logger.error(f"{str(e)}")
            raise

    def calculate_delivery_fee_distance(self, distance):
        """Calculates the delivery fee based on the delivery distance."""
        try:
            if distance < self.MIN_DISTANCE_DELIVERY:
                return self.MIN_DISTANCE_DELIVERY_FEE
            cost = math.ceil(distance / self.DISTANCE_THRESHOLD)
            return cost * 100
        except Exception as e:
            logger.error(f"{str(e)}")
            raise

    def calculate_surcharge_items(self, items):
        """Calculates the surcharge based on the number of items."""
        try:
            cost = 0
            if items <= self.SURCHARGE_ITEM_THRESHOLD:
                return 0
            if items > self.BULK_FEE_THRESHOLD:
                cost = self.COST_BULK_FEE
            cost = (items - self.SURCHARGE_ITEM_THRESHOLD) * self.COST_SURCHARGE_ITEM + cost
            return cost
        except Exception as e:
            logger.error(f"{str(e)}")
            raise

    def calculate_time(self, time):
        """Checks if the delivery falls within the rush hour."""
        try:
            time_object = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
            day_of_the_week = time_object.strftime("%A")
            hour = time_object.hour
            if day_of_the_week == self.RUSH_HOUR_DAY and self.RUSH_HOUR_START <= hour <= self.RUSH_HOUR_END:
                return True
            return False
        except Exception as e:
            logger.error(f"{str(e)}")
            raise

