from django import forms
from datetime import datetime

class DeliveryForm(forms.Form):
    cart_value = forms.IntegerField()
    delivery_distance = forms.IntegerField()
    number_of_items = forms.IntegerField()
    time = forms.CharField()

    def clean(self):
        """Override the clean method to perform additional validation."""
        cleaned_data = super().clean()
        expected_fields = set(['cart_value', 'delivery_distance', 'number_of_items', 'time'])
        actual_fields = set(self.data.keys())
        if actual_fields != expected_fields:
            raise forms.ValidationError("Invalid fields")
        return cleaned_data

    def clean_time(self):
        """Validate the 'time' field."""
        time = self.cleaned_data['time']
        if not isinstance(time, str):
            raise forms.ValidationError("Field 'time' must be a string")
        try:
            datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise forms.ValidationError("Invalid time format")
        return time

    def clean_numeric_fields(self, field_name):
        """Validate numeric fields."""
        value = self.cleaned_data.get(field_name)
        if not isinstance(value, int):
            raise forms.ValidationError(f"Field '{field_name}' must be an integer")
        if value <= 0:
            raise forms.ValidationError(f"Field '{field_name}' must be positive")
        return value

    def clean_cart_value(self):
        """Validate the 'cart_value' field."""
        return self.clean_numeric_fields('cart_value')

    def clean_delivery_distance(self):
        """Validate the 'delivery_distance' field."""
        return self.clean_numeric_fields('delivery_distance')

    def clean_number_of_items(self):
        """Validate the 'number_of_items' field."""
        return self.clean_numeric_fields('number_of_items')
