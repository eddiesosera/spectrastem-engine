# Use the official Python image
FROM python:3.9.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with increased timeout
RUN pip install --no-cache-dir --default-timeout=5000 -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 5000 (Heroku will set the PORT environment variable)
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_ENV=production

# Start the application with reduced Gunicorn workers
CMD ["sh", "-c", "gunicorn -w 2 -b 0.0.0.0:$PORT wsgi:app"]
