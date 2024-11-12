# engine/application.py

from flask import Flask
from api.upload_routes import upload_blueprint
from api.status_routes import status_blueprint
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Adjust origins as needed

# Set up logging
logging.basicConfig(level=logging.INFO)

# Register the API routes
app.register_blueprint(upload_blueprint)
app.register_blueprint(status_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
