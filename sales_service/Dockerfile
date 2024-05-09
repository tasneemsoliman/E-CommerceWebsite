# Use the official Python image as the base image
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

CMD ["python", "app.py"]
