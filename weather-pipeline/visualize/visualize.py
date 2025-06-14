import os
from flask import Flask, send_file, abort
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def plot():
    csv_path = '/data/processed.csv'
    img_path = '/data/plot.png'

    if not os.path.exists(csv_path):
        abort(404, description="Processed CSV not found")

    df = pd.read_csv(csv_path, parse_dates=['timestamp'])

    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['temperature'], marker='o', linestyle='-', color='blue')
    plt.title('Hourly Temperature - Delhi')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()

    return send_file(img_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

