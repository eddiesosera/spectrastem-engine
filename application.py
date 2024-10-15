from flask import Flask
from api.upload_routes import upload_blueprint
from api.processing_routes import processing_blueprint
from api.storage_routes import storage_blueprint
from api.status_routes import status_blueprint
from flask_cors import CORS
import logging

application = Flask(__name__)
CORS(application)  # Enable CORS for cross-origin requests

# Set up logging
logging.basicConfig(level=logging.INFO)

# Register the API routes
application.register_blueprint(upload_blueprint)
application.register_blueprint(processing_blueprint)
application.register_blueprint(storage_blueprint)
application.register_blueprint(status_blueprint)

if __name__ == '__main__':
    application.run(debug=True)
