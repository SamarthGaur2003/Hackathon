import os
from flask import Flask, send_file, abort
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def plot():
    csv_path = '/data/processed.csv'
    img_path = '/data/plot.png'

    # Ensure the data file exists
    if not os.path.exists(csv_path):
        abort(404, description="Processed CSV not found")

    # Load, plot and save
    df = pd.read_csv(csv_path)
    plt.figure()
    df.plot(y='avg_temp_24h', title='24‑Hour Rolling Avg Temperature')
    plt.xlabel('Hour Index')
    plt.ylabel('Temperature (°C)')
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()

    # Serve the image
    return send_file(img_path, mimetype='image/png')

if __name__ == '__main__':
    # Listen on all interfaces for K8s port‑forward or service
    app.run(host='0.0.0.0', port=5000)
