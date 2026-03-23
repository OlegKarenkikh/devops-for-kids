FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENV APP_PORT=8080
ENV APP_NAME=МояКоллекция
ENV DB_PATH=/app/data/collection.db
EXPOSE 8080
CMD ["python", "app.py"]
