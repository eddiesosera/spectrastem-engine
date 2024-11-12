# engine/api/status_routes.py

from flask import Blueprint, jsonify
import logging

from utils.status_tracker import status_tracker, status_lock

status_blueprint = Blueprint('status', __name__)

@status_blueprint.route('/api/status/<track_name>', methods=['GET'])
def get_processing_status(track_name):
    track_name = track_name.strip()
    logging.info(f"Checking status for track: '{track_name}'")

    with status_lock:
        track_info = status_tracker.get(track_name)

    if not track_info:
        logging.warning(f"Track '{track_name}' not found in status tracker.")
        return jsonify({"status": "Error", "message": "Status not found"}), 404

    return jsonify(track_info), 200

# Optional: Debugging route to view all status_tracker entries
@status_blueprint.route('/api/status-tracker', methods=['GET'])
def view_status_tracker():
    with status_lock:
        return jsonify(status_tracker), 200
