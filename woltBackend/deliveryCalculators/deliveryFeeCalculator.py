import logging
import math
from datetime import datetime, time

logger = logging.getLogger('log')

class DeliveryFeeCalculator:
    """Calculates the delivery fee based on various factors."""

    MIN_CART_VALUE: int = 1000
    MIN_DISTANCE_DELIVERY: int = 1000
    DISTANCE_THRESHOLD: int = 500
    MIN_DISTANCE_DELIVERY_FEE: int = 200
    COST_SURCHARGE_ITEM: int = 50
    SURCHARGE_ITEM_THRESHOLD: int = 4
    COST_BULK_FEE: int = 120
    BULK_FEE_THRESHOLD: int = 12
    RUSH_HOUR_START: int = 15
    RUSH_HOUR_END: int = 19
    RUSH_HOUR_DAY: str = "Friday"
    SURCHARGE_RUSH_HOUR: int = 120
    MAX_DELIVERY_FEE: int = 1500

    def calculate_cost(self, data: dict) -> int:
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
                total_cost = int((total_cost * self.SURCHARGE_RUSH_HOUR) / 100)

			#Apply maximum delivery fee
            if total_cost > self.MAX_DELIVERY_FEE:
                return self.MAX_DELIVERY_FEE

            return total_cost

        except Exception as e:
            logger.error(f"{str(e)}")
            raise

    def calculate_surcharge(self, cart_value: int) -> int:
        """Calculates the surcharge based on the cart value."""
        try:
            if cart_value < self.MIN_CART_VALUE:
                return self.MIN_CART_VALUE - cart_value
            return 0
        except Exception as e:
            logger.error(f"{str(e)}")
            raise

    def calculate_delivery_fee_distance(self, distance: int) -> int:
        """Calculates the delivery fee based on the delivery distance."""
        try:
            if distance < self.MIN_DISTANCE_DELIVERY:
                return self.MIN_DISTANCE_DELIVERY_FEE
            cost = math.ceil(distance / self.DISTANCE_THRESHOLD)
            return cost * 100
        except Exception as e:
            logger.error(f"{str(e)}")
            raise

    def calculate_surcharge_items(self, items: int) -> int:
        """Calculates the surcharge based on the number of items."""
        try:
            cost: int = 0
            if items <= self.SURCHARGE_ITEM_THRESHOLD:
                return 0
            if items > self.BULK_FEE_THRESHOLD:
                cost = self.COST_BULK_FEE
            cost = (items - self.SURCHARGE_ITEM_THRESHOLD) * self.COST_SURCHARGE_ITEM + cost
            return cost
        except Exception as e:
            logger.error(f"{str(e)}")
            raise

    def calculate_time(self, time: str) -> bool:
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

