# engine/api/upload_routes.py

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from utils.aws_s3 import upload_to_s3
from audio_processing.stem_separation import separate_audio_with_demucs
from audio_processing.midi_generation import generate_midi_with_basic_pitch
import os
import logging
import uuid

from utils.status_tracker import status_tracker, status_lock

upload_blueprint = Blueprint('upload', __name__)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_blueprint.route('/api/upload-audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        logging.error("No file part in the request")
        return jsonify({"status": "Error", "message": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        logging.error("No file selected")
        return jsonify({"status": "Error", "message": "No file selected"}), 400

    # Secure and clean filename
    original_filename = secure_filename(file.filename)
    base_track_name = os.path.splitext(original_filename)[0].strip()

    # Generate a unique track ID
    unique_id = uuid.uuid4().hex
    unique_track_name = f"{base_track_name}_{unique_id}"

    # Save the file locally
    file_extension = os.path.splitext(original_filename)[1]
    file_path = os.path.join(UPLOAD_FOLDER, unique_track_name + file_extension)
    file.save(file_path)

    # Initialize processing in the status tracker with thread safety
    with status_lock:
        status_tracker[unique_track_name] = {"status": "Processing", "results": None}
        logging.info(f"Track '{unique_track_name}' is being processed. Initial status set.")
        logging.info(f"Current status_tracker: {status_tracker}")  # Added logging

    # Process the file
    try:
        responses = {}
        if request.form.get('process_stems', 'true').lower() == 'true':
            responses["stems"] = process_stems_audio(file_path, unique_track_name, 'all')
            logging.info(f"Stems processing completed for track '{unique_track_name}'.")

        if request.form.get('generate_midi', 'true').lower() == 'true':
            responses["midi"] = process_midi_audio(file_path, unique_track_name)
            logging.info(f"MIDI generation completed for track '{unique_track_name}'.")

        # Update the tracker when everything completes successfully
        with status_lock:
            status_tracker[unique_track_name] = {"status": "Completed", "results": responses}
            logging.info(f"Current status_tracker: {status_tracker}")  # Added logging
        logging.info(f"Track '{unique_track_name}' processing completed successfully. Status updated.")
        return jsonify({"status": "Uploaded", "track_name": unique_track_name}), 200

    except Exception as e:
        logging.error(f"Error processing '{unique_track_name}': {e}")
        with status_lock:
            status_tracker[unique_track_name] = {"status": "Error", "message": "Processing failed"}
            logging.info(f"Current status_tracker: {status_tracker}")  # Added logging
        return jsonify({"status": "Error", "message": "Processing failed"}), 500

# Helper functions to process audio
def process_stems_audio(file_path, track_name, stems_type):
    output_dir = f"./stems_output/{track_name}"
    separation_mode = "four_stems" if stems_type == "all" else "two_stems"
    result = separate_audio_with_demucs(file_path, separation_mode, output_dir)
    if result.returncode != 0:
        raise Exception("Demucs processing failed")

    s3_urls = upload_to_s3(output_dir, track_name, s3_subfolder='stems')
    return {"status": "Completed", "message": "Stem separation completed", "stems": s3_urls}

def process_midi_audio(file_path, track_name):
    output_dir = f"./midis/{track_name}"
    midi_file_path = generate_midi_with_basic_pitch(file_path, output_dir)
    if not midi_file_path:
        raise Exception("MIDI generation failed")

    midi_s3_urls = upload_to_s3(output_dir, track_name, s3_subfolder='midis')
    return {"status": "Completed", "message": "MIDI generation completed", "midi_files": midi_s3_urls}
