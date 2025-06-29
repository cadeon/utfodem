# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements (if you have a requirements.txt, otherwise skip this)
# COPY requirements.txt .

# Install FastAPI and Uvicorn (add other dependencies as needed)
RUN pip install --no-cache-dir fastapi uvicorn

# Copy your application code
COPY . .

# Expose port 8000 (FastAPI default)
EXPOSE 8000

# Run the app with Uvicorn
CMD ["uvicorn", "utfodem-api:app", "--host", "0.0.0.0", "--port", "8000"]
