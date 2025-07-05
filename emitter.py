#!/usr/bin/env python3
"""
PhantomStroke Ultrasonic Emitter

This module implements the Phase 1 of the PhantomStroke attack:
- Detect keystrokes in real-time
- Emit ultrasonic tones (18-22 kHz) for each keystroke
- Simulate the acoustic side-channel for MEMS gyroscope interference

Dependencies:
- pynput: For cross-platform keyboard event detection
- sounddevice + numpy: For high-quality ultrasonic tone generation
- OR pyaudio: Alternative audio library
"""

import sys
import time
import threading
import math
import random
from typing import Optional, Callable

# Try to import audio libraries (will gracefully degrade if not available)
try:
    import sounddevice as sd
    import numpy as np
    AUDIO_BACKEND = 'sounddevice'
except ImportError:
    try:
        import pyaudio
        AUDIO_BACKEND = 'pyaudio'
        sd = None
        np = None
    except ImportError:
        AUDIO_BACKEND = 'fallback'
        sd = None
        np = None
        pyaudio = None

# Try to import keyboard libraries
try:
    from pynput import keyboard
    KEYBOARD_BACKEND = 'pynput'
except ImportError:
    try:
        import keyboard as keyboard_lib
        KEYBOARD_BACKEND = 'keyboard'
        keyboard = None
    except ImportError:
        KEYBOARD_BACKEND = 'fallback'
        keyboard = None
        keyboard_lib = None


class UltrasonicEmitter:
    """
    Ultrasonic tone emitter for PhantomStroke attack simulation.
    
    Generates ultrasonic tones in the 18-22 kHz range to potentially
    interfere with MEMS gyroscopes in nearby smartphones.
    """
    
    def __init__(self, 
                 frequency_range: tuple = (18000, 22000),
                 duration: float = 0.1,
                 volume: float = 0.7,
                 sample_rate: int = 44100):
        """
        Initialize the ultrasonic emitter.
        
        Args:
            frequency_range: Tuple of (min_freq, max_freq) in Hz
            duration: Duration of each tone in seconds  
            volume: Volume level (0.0 to 1.0)
            sample_rate: Audio sample rate in Hz
        """
        self.frequency_range = frequency_range
        self.duration = duration
        self.volume = volume
        self.sample_rate = sample_rate
        self.is_running = False
        self.keyboard_listener = None
        
        # Initialize audio backend
        self._init_audio_backend()
        
        print(f"[PhantomStroke] Initialized with {AUDIO_BACKEND} audio backend")
        print(f"[PhantomStroke] Frequency range: {frequency_range[0]}-{frequency_range[1]} Hz")
        print(f"[PhantomStroke] Tone duration: {duration}s")
    
    def _init_audio_backend(self):
        """Initialize the appropriate audio backend."""
        if AUDIO_BACKEND == 'sounddevice' and sd is not None:
            # Sounddevice is available - highest quality
            pass
        elif AUDIO_BACKEND == 'pyaudio' and pyaudio is not None:
            # PyAudio fallback
            self.audio = pyaudio.PyAudio()
        else:
            # Fallback mode - will simulate but not actually play audio
            print("[WARNING] No audio libraries available. Running in simulation mode.")
    
    def generate_ultrasonic_tone(self, frequency: Optional[float] = None) -> bool:
        """
        Generate and play an ultrasonic tone.
        
        Args:
            frequency: Specific frequency to play, or None for random in range
            
        Returns:
            True if tone was played successfully, False otherwise
        """
        if frequency is None:
            # Random frequency within the ultrasonic range
            frequency = random.uniform(*self.frequency_range)
        
        print(f"[PhantomStroke] Emitting {frequency:.0f} Hz tone for {self.duration}s")
        
        if AUDIO_BACKEND == 'sounddevice' and sd is not None and np is not None:
            return self._play_tone_sounddevice(frequency)
        elif AUDIO_BACKEND == 'pyaudio' and pyaudio is not None:
            return self._play_tone_pyaudio(frequency)
        else:
            return self._simulate_tone(frequency)
    
    def _play_tone_sounddevice(self, frequency: float) -> bool:
        """Play tone using sounddevice library."""
        try:
            # Generate sine wave
            t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), False)
            wave = self.volume * np.sin(2 * np.pi * frequency * t)
            
            # Play the tone
            sd.play(wave, self.sample_rate)
            sd.wait()  # Wait until finished
            return True
        except Exception as e:
            print(f"[ERROR] Failed to play tone with sounddevice: {e}")
            return False
    
    def _play_tone_pyaudio(self, frequency: float) -> bool:
        """Play tone using pyaudio library."""
        try:
            # Generate sine wave data
            frames_per_buffer = 1024
            frames = int(self.sample_rate * self.duration)
            
            # Open audio stream
            stream = self.audio.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self.sample_rate,
                output=True,
                frames_per_buffer=frames_per_buffer
            )
            
            # Generate and play audio
            for i in range(0, frames, frames_per_buffer):
                chunk_frames = min(frames_per_buffer, frames - i)
                t_start = i / self.sample_rate
                t_end = (i + chunk_frames) / self.sample_rate
                
                # Generate sine wave chunk
                chunk_data = []
                for j in range(chunk_frames):
                    t = t_start + (j / self.sample_rate)
                    sample = self.volume * math.sin(2 * math.pi * frequency * t)
                    chunk_data.append(sample)
                
                # Convert to bytes and play
                audio_data = bytes(int(sample * 32767) for sample in chunk_data)
                stream.write(audio_data)
            
            stream.stop_stream()
            stream.close()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to play tone with pyaudio: {e}")
            return False
    
    def _simulate_tone(self, frequency: float) -> bool:
        """Simulate tone playing (fallback when no audio libraries available)."""
        print(f"[SIMULATION] Would play {frequency:.0f} Hz ultrasonic tone")
        time.sleep(self.duration)
        return True
    
    def on_key_press(self, key):
        """
        Callback function for key press events.
        
        Args:
            key: The key that was pressed
        """
        try:
            # Get key character or special key name
            if hasattr(key, 'char') and key.char is not None:
                key_name = key.char
            else:
                key_name = str(key).replace('Key.', '')
            
            print(f"[PhantomStroke] Key pressed: {key_name}")
            
            # Emit ultrasonic tone in a separate thread to avoid blocking
            tone_thread = threading.Thread(target=self.generate_ultrasonic_tone)
            tone_thread.daemon = True
            tone_thread.start()
            
        except AttributeError as e:
            print(f"[ERROR] Key processing error: {e}")
    
    def on_key_release(self, key):
        """
        Callback function for key release events.
        
        Args:
            key: The key that was released
        """
        # Exit on ESC key
        if hasattr(key, 'name') and key.name == 'esc':
            print("[PhantomStroke] ESC pressed, stopping emitter...")
            return False
        elif str(key) == 'Key.esc':
            print("[PhantomStroke] ESC pressed, stopping emitter...")
            return False
    
    def start_monitoring(self):
        """Start monitoring keyboard input and emitting ultrasonic tones."""
        print("[PhantomStroke] Starting keyboard monitoring...")
        print("[PhantomStroke] Press ESC to stop")
        
        self.is_running = True
        
        if KEYBOARD_BACKEND == 'pynput' and keyboard is not None:
            self._start_pynput_monitoring()
        elif KEYBOARD_BACKEND == 'keyboard' and keyboard_lib is not None:
            self._start_keyboard_monitoring()
        else:
            self._start_fallback_monitoring()
    
    def _start_pynput_monitoring(self):
        """Start monitoring using pynput library."""
        try:
            with keyboard.Listener(
                on_press=self.on_key_press,
                on_release=self.on_key_release
            ) as listener:
                self.keyboard_listener = listener
                listener.join()
        except Exception as e:
            print(f"[ERROR] Pynput monitoring failed: {e}")
            self._start_fallback_monitoring()
    
    def _start_keyboard_monitoring(self):
        """Start monitoring using keyboard library."""
        try:
            def on_key_event(event):
                if event.event_type == keyboard_lib.KEY_DOWN:
                    print(f"[PhantomStroke] Key pressed: {event.name}")
                    tone_thread = threading.Thread(target=self.generate_ultrasonic_tone)
                    tone_thread.daemon = True
                    tone_thread.start()
                elif event.event_type == keyboard_lib.KEY_UP and event.name == 'esc':
                    print("[PhantomStroke] ESC pressed, stopping emitter...")
                    self.is_running = False
                    return False
            
            keyboard_lib.hook(on_key_event)
            keyboard_lib.wait('esc')
        except Exception as e:
            print(f"[ERROR] Keyboard library monitoring failed: {e}")
            self._start_fallback_monitoring()
    
    def _start_fallback_monitoring(self):
        """Fallback monitoring using input() for demonstration."""
        print("[WARNING] No keyboard libraries available. Using fallback input mode.")
        print("Type characters and press Enter to simulate keystrokes (type 'quit' to exit):")
        
        try:
            while self.is_running:
                user_input = input("> ")
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                # Simulate each character as a keystroke
                for char in user_input:
                    print(f"[PhantomStroke] Simulated key: {char}")
                    self.generate_ultrasonic_tone()
                    time.sleep(0.1)  # Small delay between characters
                
        except KeyboardInterrupt:
            print("\n[PhantomStroke] Interrupted by user")
        
        self.is_running = False
    
    def stop_monitoring(self):
        """Stop keyboard monitoring."""
        self.is_running = False
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        # Clean up audio resources
        if AUDIO_BACKEND == 'pyaudio' and hasattr(self, 'audio'):
            self.audio.terminate()
    
    def test_tone_generation(self):
        """Test the ultrasonic tone generation across the frequency range."""
        print("[PhantomStroke] Testing ultrasonic tone generation...")
        
        test_frequencies = [18000, 19000, 20000, 21000, 22000]
        
        for freq in test_frequencies:
            print(f"Testing {freq} Hz...")
            success = self.generate_ultrasonic_tone(freq)
            if not success:
                print(f"Failed to generate {freq} Hz tone")
            time.sleep(0.5)
        
        print("Tone generation test completed.")


def main():
    """Main function to run the ultrasonic emitter."""
    print("=" * 60)
    print("PhantomStroke Ultrasonic Emitter v1.0")
    print("Phase 1: Acoustic Side-Channel Attack Simulation")
    print("=" * 60)
    print()
    
    # Print backend information
    print(f"Audio Backend: {AUDIO_BACKEND}")
    print(f"Keyboard Backend: {KEYBOARD_BACKEND}")
    print()
    
    # Create emitter instance
    emitter = UltrasonicEmitter(
        frequency_range=(18000, 22000),
        duration=0.1,
        volume=0.7
    )
    
    try:
        # Test tone generation first
        if len(sys.argv) > 1 and sys.argv[1] == '--test':
            emitter.test_tone_generation()
        else:
            # Start real-time monitoring
            emitter.start_monitoring()
    
    except KeyboardInterrupt:
        print("\n[PhantomStroke] Shutting down...")
    
    finally:
        emitter.stop_monitoring()
        print("[PhantomStroke] Emitter stopped.")


if __name__ == "__main__":
    main()