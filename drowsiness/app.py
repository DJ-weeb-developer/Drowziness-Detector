from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
from drowsiness_detector import DrowsinessDetector

app = Flask(__name__)

# Global camera object and detector
camera = None
detector = DrowsinessDetector()
is_running = False
camera_lock = threading.Lock()

def get_camera():
    global camera
    if camera is None:
        print("Initializing camera...")
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("ERROR: Could not open camera!")
    return camera

def stop_camera():
    global camera
    print("Stopping camera...")
    if camera is not None:
        camera.release()
        camera = None

def generate_frames():
    global is_running, camera
    print("Starting frame generation loop...")
    camera = get_camera()
    
    while is_running:
        success, frame = camera.read()
        if not success:
            print("Failed to read frame")
            break
        
        # Process frame with Drowsiness Detector
        frame = detector.process_frame(frame)
        
        # Encode
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    # If loop exits, ensure we don't hold the camera if needed,
    # but usually we keep it open for quick restart. 
    # For now, let's just show a black frame or stop yielding.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/start', methods=['POST'])
def start_camera():
    global is_running
    is_running = True
    return jsonify({"status": "started"})

@app.route('/api/stop', methods=['POST'])
def stop_stream():
    global is_running
    is_running = False
    return jsonify({"status": "stopped"})

@app.route('/api/settings', methods=['POST'])
def update_settings():
    data = request.json
    threshold = data.get('threshold')
    frames = data.get('frames')
    detector.update_settings(threshold, frames)
    return jsonify({"status": "updated"})

@app.route('/api/stats')
def get_stats():
    return jsonify({
        "ear": detector.current_ear,
        "blinks": detector.total_blinks,
        "status": detector.status,
        "fatigue_duration": detector.fatigue_duration
    })

if __name__ == '__main__':
    try:
        app.run(debug=True, threaded=True, port=5001)
    finally:
        stop_camera()
        detector.close()
