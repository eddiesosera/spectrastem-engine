# Uses the official Python image
FROM python:3.9-slim

# Sets the working directory in the container
WORKDIR /app

# Copies requirements.txt to the container
COPY requirements.txt .

# Installs Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copies the current directory contents into the container at /app
COPY . .

# Exposes port 5000 (Heroku will override this with $PORT)
EXPOSE 5000

# Sets environment variables for Flask
ENV FLASK_ENV=production

# Sets the entry point to Gunicorn (as indicated in your Procfile)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "wsgi:app"]
