FROM python:3.9-slim
WORKDIR /app
COPY visualize.py .
RUN pip install flask pandas matplotlib
VOLUME /data
EXPOSE 5000
CMD ["python", "visualize.py"]