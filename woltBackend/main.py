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
        '{"a": 10, "b": 20, "c": "example"}',
        'http://localhost:8000/calculate/'
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(e.stderr)

if __name__ == "__main__":
    send_curl_request()
