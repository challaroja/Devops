# Python official lightweight image
FROM python:3.10-slim

# Working directory set cheyali
WORKDIR /app

# Requirements file copy chesi dependencies install cheyali
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Project files and folders motham copy cheyali
COPY . .

# FastAPI app run avvadaniki port expose cheyali
EXPOSE 8001

# Server start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]