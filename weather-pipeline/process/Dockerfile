FROM python:3.9-slim
WORKDIR /app
COPY process.py .
RUN pip install pandas
VOLUME /data
CMD ["python", "process.py"]