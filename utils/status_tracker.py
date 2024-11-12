# processing_status = {}
# status_registry = {}

# def update_status(track_name, status, current_step, stems=None, midi=None):
#     """
#     Update the processing status for a given track.

#     Args:
#         track_name (str): The name of the track being processed.
#         status (str): The overall status of the processing (e.g., "Processing", "Completed", "Failed").
#         current_step (str): The current step of the process.
#         stems (dict, optional): The URLs of the processed stems.
#         midi (dict, optional): The URLs of the generated MIDI files.
#     """
#     # Update the status information
#     status_registry[track_name] = {
#         "status": status,
#         "current_step": current_step
#     }

#     if stems:
#         status_registry[track_name]["stems"] = stems

#     if midi:
#         status_registry[track_name]["midi"] = midi

# def get_status(track_name):
#     return processing_status.get(track_name, {"status": "Not Found"})
# File: engine/utils/status_tracker.py

# File: engine/utils/status_tracker.py

import threading

# A thread-safe dictionary to track the status of each processing task
status_tracker = {}

# A lock to ensure thread-safe operations on status_tracker
status_lock = threading.Lock()

def update_status(track_name, status, results=None):
    """
    Update the status of a given track in the status_tracker.

    Args:
        track_name (str): The unique name of the track.
        status (str): The current status (e.g., "Processing", "Completed", "Error").
        results (dict, optional): The results of the processing. Defaults to None.
    """
    with status_lock:
        status_tracker[track_name] = {"status": status, "results": results}
