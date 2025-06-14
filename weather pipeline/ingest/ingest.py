import os
import requests
import json

def main():
    # You can also supply the key via the OPENWEATHER_API_KEY env var;
    # if that is not set, we fall back to your provided key:
    API_KEY = os.getenv('OPENWEATHER_API_KEY', 'f784ba74e2c065182d499816553355d8')

    # Build the request URL
    url = (
        "https://api.openweathermap.org/data/2.5/forecast"
        "?latitude=28.67&longitude=77.22"
        "&hourly=temperature_2m"
        f"&appid={API_KEY}"
    )

    # Fetch & dump to shared volume
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    with open('/data/weather.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    main()
