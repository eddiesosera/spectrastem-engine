# Stage 1: Build Stage
FROM python:3.9.13-slim AS builder

# Install system dependencies required for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir --default-timeout=5000 -r requirements.txt

# Copy application code
COPY . .

# Remove unnecessary files
RUN rm -rf tests/ docs/ media/ uploads/ stems_output/ outputs/ tmp/

# Stage 2: Final Stage
FROM python:3.9.13-slim

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the dependencies from the builder stage
COPY --from=builder /root/.local /root/.local

# Copy the application code from the builder stage
COPY --from=builder /app /app

# Set PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production

# Start the application
CMD ["sh", "-c", "gunicorn -w 2 -b 0.0.0.0:$PORT application:app"]
