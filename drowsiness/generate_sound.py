import numpy as np
from scipy.io.wavfile import write

def generate_beep(filename="alert.wav", duration=1.0, frequency=1000):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Generate sine wave
    note = np.sin(frequency * t * 2 * np.pi)
    
    # Normalize to 16-bit range
    audio = note * (2**15 - 1)
    
    write(filename, sample_rate, audio.astype(np.int16))
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_beep()
