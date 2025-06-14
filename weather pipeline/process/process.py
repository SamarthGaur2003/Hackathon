import json
import pandas as pd

def main():
    # Read the raw JSON
    with open('/data/weather.json', 'r') as f:
        data = json.load(f)

    # Extract the hourly temp list
    temps = data['hourly']['temperature_2m']
    df = pd.DataFrame({ 'temperature': temps })

    # Compute a 24‑hour rolling average
    df['avg_temp_24h'] = df['temperature'].rolling(window=24, min_periods=1).mean()

    # Write out a CSV for the next step
    df.to_csv('/data/processed.csv', index=False)

if __name__ == '__main__':
    main()
