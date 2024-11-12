# File: engine/api/events.py
from flask_socketio import emit, join_room, leave_room
from flask import session
from . import socketio

@socketio.on('connect', namespace='/status')
def handle_connect():
    # Join a room based on session ID or any unique identifier
    room = session.get('room')
    if room:
        join_room(room)
    emit('status', {'message': 'Connected to status updates.'})

@socketio.on('disconnect', namespace='/status')
def handle_disconnect():
    room = session.get('room')
    if room:
        leave_room(room)
    emit('status', {'message': 'Disconnected from status updates.'})
