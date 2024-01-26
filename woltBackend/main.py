import subprocess

def send_curl_request():
    command = [
        'curl',
        '-X',
        'POST',
        '-H',
        'Content-Type: application/json',
        '-d',
        # '{"invalid": "data"}',
        # '{"a": 10, "b": 20, "c": "example"}',
        # '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": "4", "time": "2024-01-15T13:00:00Z", "test": "test" }',
        # '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": "4"}',
        '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": "4", "time": "2024-01-15T13:00:00Z"}',
        'http://localhost:8000/deliveryCalculator/'
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(e.stderr)

if __name__ == "__main__":
    send_curl_request()
