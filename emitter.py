"""
PhantomStroke Emitter with Fixed Key-to-Frequency Mapping
Each key emits a consistent ultrasonic tone (18–22 kHz) for ML recovery.
"""

import numpy as np
import sounddevice as sd
from pynput import keyboard
import threading
import time

# Fixed frequency mapping (example: 26 lowercase letters)
KEY_FREQUENCIES = {
    'a': 18000, 'b': 18150, 'c': 18300, 'd': 18450,
    'e': 18600, 'f': 18750, 'g': 18900, 'h': 19050,
    'i': 19200, 'j': 19350, 'k': 19500, 'l': 19650,
    'm': 19800, 'n': 19950, 'o': 20100, 'p': 20250,
    'q': 20400, 'r': 20550, 's': 20700, 't': 20850,
    'u': 21000, 'v': 21150, 'w': 21300, 'x': 21450,
    'y': 21600, 'z': 21750
}

DURATION = 0.1          # seconds
VOLUME = 0.7            # amplitude
SAMPLE_RATE = 44100     # Hz

def play_tone(frequency: float):
    """Generate and play a sine wave of the given frequency."""
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), False)
    wave = VOLUME * np.sin(2 * np.pi * frequency * t)
    sd.play(wave, SAMPLE_RATE)
    sd.wait()

def emit_tone_for_key(key_name: str):
    """Emit tone corresponding to a specific key."""
    freq = KEY_FREQUENCIES.get(key_name.lower())
    if freq:
        print(f"[PhantomStroke] Key: {key_name} → {freq} Hz")
        threading.Thread(target=play_tone, args=(freq,), daemon=True).start()
    else:
        print(f"[Ignored] Key: {key_name}")

def on_press(key):
    """Detect keypress and emit fixed-frequency tone."""
    try:
        if hasattr(key, 'char') and key.char:
            emit_tone_for_key(key.char)
    except Exception as e:
        print(f"[Error] {e}")

def on_release(key):
    """Stop on ESC."""
    if key == keyboard.Key.esc:
        print("[PhantomStroke] ESC pressed. Exiting.")
        return False

def main():
    print("=" * 50)
    print("PhantomStroke: Fixed Frequency Emitter")
    print("Press a-z to emit unique tones")
    print("Press ESC to stop")
    print("=" * 50)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
