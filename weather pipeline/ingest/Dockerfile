FROM python:3.9-slim
WORKDIR /app
COPY ingest.py .
RUN pip install requests
VOLUME /data
CMD ["python", "ingest.py"]