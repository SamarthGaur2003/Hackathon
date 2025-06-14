import os
import requests
import json

def main():
    API_KEY = os.getenv('OPENWEATHER_API_KEY', 'f784ba74e2c065182d499816553355d8')
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Delhi&units=metric&appid={API_KEY}"

    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    with open('/data/weather.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    main()


