import cv2
import mediapipe as mp
import numpy as np
import time
from audio_alert import AudioAlert

# MediaPipe Face Mesh Init
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class DrowsinessDetector:
    def __init__(self):
        # Configuration (Default values, can be updated)
        self.EAR_THRESHOLD = 0.25  # Eye Aspect Ratio threshold
        self.CONSEC_FRAMES_DROWSY = 20 # Number of frames eyes closed to trigger drowsiness
        self.EAR_CONSEC_FRAMES_BLINK = 1 # Minimum frames for a blink (fast)
        
        # State
        self.counter = 0
        self.total_blinks = 0
        self.alarm_on = False
        self.status = "ACTIVE"
        self.current_ear = 0.0
        self.drowsy_start_time = None
        self.fatigue_duration = 0.0
        
        # Audio
        self.audio_alert = AudioAlert()

        # Face Mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Indices for Left and Right Eye (MediaPipe Face Mesh)
        # Left Eye: 362, 385, 387, 263, 373, 380
        # Right Eye: 33, 160, 158, 133, 153, 144
        self.LEFT_EYE_IDXS = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE_IDXS = [33, 160, 158, 133, 153, 144]

    def calculate_ear(self, eye_landmarks, w, h):
        # eye_landmarks is a list of (x, y) coordinates
        # Vertical distances
        A = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        B = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        # Horizontal distance
        C = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])

        # Compute EAR
        ear = (A + B) / (2.0 * C)
        return ear

    def update_settings(self, new_threshold, new_bg_frames):
        if new_threshold:
            self.EAR_THRESHOLD = float(new_threshold)
        if new_bg_frames:
            self.CONSEC_FRAMES_DROWSY = int(new_bg_frames)

    def process_frame(self, frame):
        try:
            # 1. FPS Optimization: Resize frame
            frame = cv2.resize(frame, (640, 480))
            h, w, c = frame.shape

            # 2. Lighting Normalization: CLAHE
            # Convert to LAB color space
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            # Apply CLAHE to L-channel
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            # Merge and convert back to RGB
            limg = cv2.merge((cl, a, b))
            final_frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            rgb_frame = cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB)
            
            results = self.face_mesh.process(rgb_frame)
            
            self.current_ear = 0.0
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    landmarks = face_landmarks.landmark
                    
                    # Extract coordinates for left and right eyes
                    left_eye_pts = np.array([(landmarks[i].x * w, landmarks[i].y * h) for i in self.LEFT_EYE_IDXS])
                    right_eye_pts = np.array([(landmarks[i].x * w, landmarks[i].y * h) for i in self.RIGHT_EYE_IDXS])

                    # Calculate EAR
                    leftEAR = self.calculate_ear(left_eye_pts, w, h)
                    rightEAR = self.calculate_ear(right_eye_pts, w, h)

                    # Average EAR
                    self.current_ear = (leftEAR + rightEAR) / 2.0

                    # Draw Eyes
                    cv2.polylines(frame, [left_eye_pts.astype(int)], True, (0, 255, 0), 1)
                    cv2.polylines(frame, [right_eye_pts.astype(int)], True, (0, 255, 0), 1)

                    # Check drowsiness
                    if self.current_ear < self.EAR_THRESHOLD:
                        self.counter += 1

                        if self.counter >= self.CONSEC_FRAMES_DROWSY:
                            if not self.alarm_on:
                                self.alarm_on = True
                                self.audio_alert.start_alarm()
                                self.drowsy_start_time = time.time() # Start tracking duration
                                
                            self.status = "DROWSINESS DETECTED"
                            
                            # Update duration
                            if self.drowsy_start_time:
                                self.fatigue_duration = time.time() - self.drowsy_start_time
                            
                            cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    else:
                        # If previously eyes were closed and now open, check if it was a blink
                        # Simplification: If counter was small but > blink threshold, count as blink
                        if self.CONSEC_FRAMES_DROWSY > self.counter > self.EAR_CONSEC_FRAMES_BLINK:
                             self.total_blinks += 1

                        self.counter = 0
                        self.alarm_on = False
                        self.audio_alert.stop_alarm()
                        self.status = "Active"
                        self.drowsy_start_time = None 
                        self.fatigue_duration = 0.0

                    # Info on Screen
                    cv2.putText(frame, f"EAR: {self.current_ear:.2f}", (w - 150, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(frame, f"Blinks: {self.total_blinks}", (10, h - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                                
        except Exception as e:
            print(f"Error processing frame: {e}")
            # Identify error on frame if possible
            cv2.putText(frame, "Error in detection", (10, h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        return frame

    def close(self):
        self.face_mesh.close()
        self.audio_alert.stop_alarm()
