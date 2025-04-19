FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

ENV MQTT_BROKER=mosquitto
ENV MQTT_PORT=1883
ENV MQTT_USERNAME=
ENV MQTT_PASSWORD=
ENV WEBHOOK_URL=
ENV CAR_ID=1

CMD ["python", "app.py"]
