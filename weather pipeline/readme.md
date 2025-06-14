## Cloud-Native Weather Data Pipeline: Step-by-Step Guide

This guide will help you build a complete cloud-native data pipeline using a public weather API. We will:

1. **Set up your environment**
2. **Write ingestion, processing, and visualization scripts**
3. **Containerize each component**
4. **Define and deploy an Argo Workflows pipeline**
5. **Verify and present results**

---

### 1. Prerequisites

* **Basic Tools**: Git, Docker, Python 3.8+
* **Kubernetes Cluster**: Minikube or a remote K8s cluster
* **Argo Workflows**: Installed on your cluster
* **DockerHub Account**: To push your images
* **IDE or Text Editor**: VS Code, Sublime, etc.

> **Note:** If any of these are new, follow the installation links in the \[Appendix].

---

### 2. Choose Weather API & Define Pipeline Stages

**API:** `https://api.open-meteo.com/v1/forecast?latitude=28.67&longitude=77.22&hourly=temperature_2m`

**Pipeline Stages**:

1. **Ingestion**: Fetch JSON data from Open-Meteo
2. **Processing**: Extract hourly temperatures, compute average
3. **Visualization**: Generate a plot image and serve via a simple Flask app

---

### 3. Project Structure

```
weather-pipeline/
├── ingest/
│   ├── Dockerfile
│   └── ingest.py
├── process/
│   ├── Dockerfile
│   └── process.py
├── visualize/
│   ├── Dockerfile
│   └── visualize.py
├── workflow.yaml
└── README.md
```

---

### 4. Step-by-Step Implementation

#### 4.1 Ingestion

* **File:** `ingest/ingest.py`

```python
import requests, json

def main():
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.67&longitude=77.22&hourly=temperature_2m"
    resp = requests.get(url)
    data = resp.json()
    with open('/data/weather.json', 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    main()
```

* **Dockerfile:** `ingest/Dockerfile`

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY ingest.py .
RUN pip install requests
VOLUME /data
CMD ["python", "ingest.py"]
```

#### 4.2 Processing

* **File:** `process/process.py`

```python
import json
import pandas as pd

def main():
    with open('/data/weather.json') as f:
        data = json.load(f)
    temps = data['hourly']['temperature_2m']
    df = pd.DataFrame({ 'temperature': temps })
    df['avg_temp_24h'] = df['temperature'].rolling(window=24).mean()
    df.to_csv('/data/processed.csv', index=False)

if __name__ == '__main__':
    main()
```

* **Dockerfile:** `process/Dockerfile`

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY process.py .
RUN pip install pandas
VOLUME /data
CMD ["python", "process.py"]
```

#### 4.3 Visualization

* **File:** `visualize/visualize.py`

```python
from flask import Flask, send_file
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def plot():
    df = pd.read_csv('/data/processed.csv')
    plt.figure()
    df.plot(y='avg_temp_24h')
    plt.savefig('/data/plot.png')
    return send_file('/data/plot.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

* **Dockerfile:** `visualize/Dockerfile`

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY visualize.py .
RUN pip install flask pandas matplotlib
VOLUME /data
EXPOSE 5000
CMD ["python", "visualize.py"]
```

---

### 5. Build & Push Docker Images

```bash
# Ingest image
docker build -t <dockerhub-username>/weather-ingest:latest ./ingest
# Process image

docker build -t <dockerhub-username>/weather-process:latest ./process
# Visualize image
docker build -t <dockerhub-username>/weather-visualize:latest ./visualize

# Push all
for img in weather-ingest weather-process weather-visualize; do
  docker push <dockerhub-username>/$img:latest
done
```

---

### 6. Define Argo Workflow

* **File:** `workflow.yaml`

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: weather-pipeline-
spec:
  entrypoint: main
  templates:
  - name: main
    steps:
    - - name: ingest
        template: ingest
    - - name: process
        template: process
    - - name: visualize
        template: visualize

  - name: ingest
    container:
      image: <dockerhub-username>/weather-ingest:latest
      volumeMounts:
      - name: data
        mountPath: /data

  - name: process
    container:
      image: <dockerhub-username>/weather-process:latest
      volumeMounts:
      - name: data
        mountPath: /data

  - name: visualize
    container:
      image: <dockerhub-username>/weather-visualize:latest
      volumeMounts:
      - name: data
        mountPath: /data
      ports:
      - containerPort: 5000

  volumes:
  - name: data
    emptyDir: {}
```

---

### 7. Deploy & Run

1. **Submit Workflow**:

   ```bash
   kubectl create namespace argo
   kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo-workflows/stable/manifests/install.yaml
   argo submit --watch -n argo workflow.yaml
   ```
2. **Expose Visualization**:

   ```bash
   kubectl port-forward -n argo svc/argo-server 2746:2746 &
   argo port-forward workflow/<workflow-name> 5000:5000 -n argo
   # Visit http://localhost:5000 in your browser
   ```

---

### 8. Presentation & Next Steps

* **Screenshots**: Argo UI, logs, deployed Flask plot
* **Live Demo**: Show graph in browser
* **README.md**: Document all steps

---

## Appendix

* **Git**: [https://git-scm.com/book/en/v2](https://git-scm.com/book/en/v2)
* **Docker**: [https://docs.docker.com/get-started/](https://docs.docker.com/get-started/)
* **Minikube**: [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/)
* **Argo Workflows**: [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
