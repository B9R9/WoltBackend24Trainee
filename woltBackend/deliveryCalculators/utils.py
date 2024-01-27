from django import forms
from datetime import datetime

class DeliveryForm(forms.Form):
    cart_value = forms.IntegerField()
    delivery_distance = forms.IntegerField()
    number_of_items = forms.IntegerField()
    time = forms.CharField()

    def clean(self) -> dict:
        """Override the clean method to perform additional validation."""
        cleaned_data: dict = super().clean()
        expected_fields :set = set(['cart_value', 'delivery_distance', 'number_of_items', 'time'])
        actual_fields: set = set(self.data.keys())
        if actual_fields != expected_fields:
            raise forms.ValidationError("Invalid fields")
        return cleaned_data
#Check UTC time
    def clean_time(self) -> str:
        """Validate the 'time' field."""
        time: str = self.cleaned_data['time']
        if not isinstance(time, str):
            raise forms.ValidationError("Field 'time' must be a string")
        try:
            datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise forms.ValidationError("Invalid time format")
        return time

    def clean_numeric_fields(self, field_name: str) -> int:
        """Validate numeric fields."""
        value: int = self.cleaned_data.get(field_name)
        if not isinstance(value, int):
            raise forms.ValidationError(f"Field '{field_name}' must be an integer")
        if value <= 0:
            raise forms.ValidationError(f"Field '{field_name}' must be positive")
        return value

    def clean_cart_value(self)-> int:
        """Validate the 'cart_value' field."""
        return self.clean_numeric_fields('cart_value')

    def clean_delivery_distance(self) -> int:
        """Validate the 'delivery_distance' field."""
        return self.clean_numeric_fields('delivery_distance')

    def clean_number_of_items(self) -> int:
        """Validate the 'number_of_items' field."""
        return self.clean_numeric_fields('number_of_items')
