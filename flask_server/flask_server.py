from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='out')
socketio = SocketIO(app, cors_allowed_origins="*")

# Serve the main page
@app.route('/')
def index():
    return send_from_directory('out', 'index.html')

# Route for serving Next.js static files (JavaScript, chunks)
@app.route('/_next/static/<path:filename>')
def next_static(filename):
    return send_from_directory('out/_next/static', filename)

# Route for serving other _next assets (e.g., manifest)
@app.route('/_next/<path:filename>')
def next_assets(filename):
    return send_from_directory('out/_next', filename)

# Route for serving CSS files
@app.route('/css/<path:filename>')
def css_files(filename):
    return send_from_directory('out/_next/static/css', filename)

# Route for serving media files (e.g., fonts)
@app.route('/media/<path:filename>')
def media_files(filename):
    return send_from_directory('out/_next/static/media', filename)

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('response', {'message': 'Connected to Flask WebSocket server!'})

@socketio.on('slide_change')
def handle_slide_change(data):
    print(f"Slide changed to: {data['currentSlide']}")
    emit('update_slide', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
