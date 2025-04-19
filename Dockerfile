FROM python:3.13-slim
LABEL org.opencontainers.image.source https://github.com/eden881/trmnl-teslamate-reporter
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
