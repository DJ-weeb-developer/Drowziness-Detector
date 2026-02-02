import threading
import time
import os

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Pygame not installed. Audio alerts will be disabled.")

class AudioAlert:
    def __init__(self, sound_file="alert.wav"):
        global PYGAME_AVAILABLE
        self.sound_file = sound_file
        self.playing = False
        self.stop_signal = False
        self._thread = None
        
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                # Create a dummy file if it doesn't exist to prevent immediate crash, 
                # though user should replace it.
                if not os.path.exists(self.sound_file):
                    print(f"Warning: {self.sound_file} not found. Audio will not play until file is present.")
                else:
                    self.sound = pygame.mixer.Sound(self.sound_file)
            except Exception as e:
                print(f"Audio init error: {e}")
                PYGAME_AVAILABLE = False

    def _loop_sound(self):
        while self.playing and not self.stop_signal:
            if PYGAME_AVAILABLE and os.path.exists(self.sound_file):
                try:
                    if not pygame.mixer.get_busy():
                        pygame.mixer.Sound(self.sound_file).play()
                    # Sleep a bit to prevent busy loop if sound is short
                    time.sleep(1.0) 
                except Exception:
                    pass
            else:
                # Mock playing
                time.sleep(1)
                
    def start_alarm(self):
        if not self.playing:
            self.playing = True
            self.stop_signal = False
            self._thread = threading.Thread(target=self._loop_sound)
            self._thread.daemon = True
            self._thread.start()

    def stop_alarm(self):
        self.playing = False
        self.stop_signal = True
        if PYGAME_AVAILABLE:
            pygame.mixer.stop()
