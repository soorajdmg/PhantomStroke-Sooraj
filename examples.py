#!/usr/bin/env python3
"""
PhantomStroke Usage Examples

This script demonstrates various ways to use the PhantomStroke ultrasonic emitter.
"""

import time
import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from emitter import UltrasonicEmitter


def example_basic_usage():
    """Example 1: Basic ultrasonic tone emission."""
    print("Example 1: Basic Ultrasonic Tone Emission")
    print("-" * 45)
    
    # Create emitter with default settings
    emitter = UltrasonicEmitter()
    
    # Generate a few test tones
    frequencies = [18000, 19000, 20000, 21000, 22000]
    
    for freq in frequencies:
        print(f"Emitting {freq} Hz tone...")
        emitter.generate_ultrasonic_tone(freq)
        time.sleep(0.5)
    
    print("Basic example completed.\n")


def example_custom_configuration():
    """Example 2: Custom emitter configuration."""
    print("Example 2: Custom Configuration")
    print("-" * 32)
    
    # Create emitter with custom settings
    emitter = UltrasonicEmitter(
        frequency_range=(19000, 21000),  # Narrower frequency range
        duration=0.2,                    # Longer tone duration
        volume=0.5,                      # Lower volume
        sample_rate=48000               # Higher sample rate
    )
    
    print("Custom emitter settings:")
    print(f"  Frequency range: {emitter.frequency_range[0]}-{emitter.frequency_range[1]} Hz")
    print(f"  Duration: {emitter.duration}s")
    print(f"  Volume: {emitter.volume}")
    print(f"  Sample rate: {emitter.sample_rate} Hz")
    
    # Generate random tones
    for i in range(3):
        print(f"Random tone {i+1}...")
        emitter.generate_ultrasonic_tone()
        time.sleep(0.3)
    
    print("Custom configuration example completed.\n")


def example_keystroke_simulation():
    """Example 3: Simulate keystroke detection."""
    print("Example 3: Keystroke Simulation")
    print("-" * 30)
    
    emitter = UltrasonicEmitter(duration=0.1)
    
    # Simulate typing a word
    word = "HELLO"
    print(f"Simulating typing: '{word}'")
    
    for i, char in enumerate(word):
        print(f"  [{i+1}] Key '{char}' -> ", end="", flush=True)
        
        # Simulate key press event
        class MockKey:
            def __init__(self, char):
                self.char = char
        
        mock_key = MockKey(char)
        emitter.on_key_press(mock_key)
        
        print("Done")
        time.sleep(0.3)
    
    print("Keystroke simulation completed.\n")


def example_frequency_sweep():
    """Example 4: Frequency sweep demonstration."""
    print("Example 4: Frequency Sweep")
    print("-" * 25)
    
    emitter = UltrasonicEmitter(duration=0.15)
    
    # Sweep from 18kHz to 22kHz
    start_freq = 18000
    end_freq = 22000
    steps = 8
    
    print(f"Sweeping from {start_freq} Hz to {end_freq} Hz in {steps} steps...")
    
    for i in range(steps + 1):
        freq = start_freq + (end_freq - start_freq) * i / steps
        print(f"  Step {i+1}/{steps+1}: {freq:.0f} Hz")
        emitter.generate_ultrasonic_tone(freq)
        time.sleep(0.2)
    
    print("Frequency sweep completed.\n")


def example_burst_pattern():
    """Example 5: Burst pattern simulation."""
    print("Example 5: Burst Pattern")
    print("-" * 22)
    
    emitter = UltrasonicEmitter(duration=0.05)  # Short bursts
    
    # Simulate rapid keystroke burst (like typing fast)
    print("Simulating rapid keystroke burst...")
    
    for burst in range(3):
        print(f"  Burst {burst+1}: ", end="", flush=True)
        
        # 5 rapid tones
        for tone in range(5):
            emitter.generate_ultrasonic_tone()
            print("♪", end="", flush=True)
            time.sleep(0.08)
        
        print(" (pause)")
        time.sleep(0.5)
    
    print("Burst pattern completed.\n")


def interactive_demo():
    """Interactive demonstration."""
    print("Interactive Demo")
    print("-" * 16)
    print("Choose an operation:")
    print("1. Single tone")
    print("2. Random tone")
    print("3. Frequency sweep")
    print("4. Exit")
    
    emitter = UltrasonicEmitter()
    
    while True:
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == '1':
                freq = input("Enter frequency (18000-22000): ")
                try:
                    freq = float(freq)
                    if 18000 <= freq <= 22000:
                        emitter.generate_ultrasonic_tone(freq)
                        print(f"✓ Played {freq} Hz tone")
                    else:
                        print("✗ Frequency out of range")
                except ValueError:
                    print("✗ Invalid frequency")
            
            elif choice == '2':
                emitter.generate_ultrasonic_tone()
                print("✓ Played random frequency tone")
            
            elif choice == '3':
                print("Playing frequency sweep...")
                for freq in range(18000, 23000, 1000):
                    emitter.generate_ultrasonic_tone(freq)
                    time.sleep(0.3)
                print("✓ Sweep completed")
            
            elif choice == '4':
                print("Exiting interactive demo.")
                break
            
            else:
                print("✗ Invalid choice")
        
        except KeyboardInterrupt:
            print("\nExiting interactive demo.")
            break


def main():
    """Run all examples."""
    print("PhantomStroke Usage Examples")
    print("=" * 40)
    print()
    
    try:
        # Run all examples
        example_basic_usage()
        example_custom_configuration()
        example_keystroke_simulation()
        example_frequency_sweep()
        example_burst_pattern()
        
        # Ask for interactive demo
        if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
            interactive_demo()
        else:
            print("Run with '--interactive' flag for interactive demo.")
    
    except KeyboardInterrupt:
        print("\nExamples interrupted.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()