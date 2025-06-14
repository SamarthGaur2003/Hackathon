import json
import pandas as pd

def main():
    with open('/data/weather.json', 'r') as f:
        data = json.load(f)

    # Extract timestamps and temperatures
    forecasts = data['list']
    times = [entry['dt_txt'] for entry in forecasts]
    temps = [entry['main']['temp'] for entry in forecasts]

    df = pd.DataFrame({
        'timestamp': pd.to_datetime(times),
        'temp': temps
    })

    # Save direct hourly temperature data
    df.to_csv('/data/processed.csv', index=False)

if __name__ == '__main__':
    main()

