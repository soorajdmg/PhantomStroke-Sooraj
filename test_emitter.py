#!/usr/bin/env python3
"""
Test script for PhantomStroke Ultrasonic Emitter
"""

import time
import sys
import os

# Add the current directory to path to import emitter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from emitter import UltrasonicEmitter


def test_emitter_basic():
    """Test basic emitter functionality."""
    print("Testing basic emitter functionality...")
    
    emitter = UltrasonicEmitter(
        frequency_range=(18000, 22000),
        duration=0.05,  # Shorter duration for testing
        volume=0.5
    )
    
    # Test tone generation
    print("Testing single tone generation...")
    success = emitter.generate_ultrasonic_tone(20000)
    assert success, "Failed to generate ultrasonic tone"
    
    # Test random frequency generation
    print("Testing random frequency generation...")
    success = emitter.generate_ultrasonic_tone()
    assert success, "Failed to generate random frequency tone"
    
    print("✓ Basic functionality test passed")


def test_emitter_frequency_range():
    """Test emitter with different frequency ranges."""
    print("Testing frequency range functionality...")
    
    # Test lower frequency range
    emitter = UltrasonicEmitter(frequency_range=(18000, 19000), duration=0.02)
    success = emitter.generate_ultrasonic_tone()
    assert success, "Failed with lower frequency range"
    
    # Test upper frequency range  
    emitter = UltrasonicEmitter(frequency_range=(21000, 22000), duration=0.02)
    success = emitter.generate_ultrasonic_tone()
    assert success, "Failed with upper frequency range"
    
    print("✓ Frequency range test passed")


def test_keyboard_simulation():
    """Test keyboard simulation functionality."""
    print("Testing keyboard simulation...")
    
    emitter = UltrasonicEmitter(duration=0.02)
    
    # Simulate key press events
    test_keys = ['a', 'b', 'c', '1', '2', '3']
    
    for key_char in test_keys:
        print(f"Simulating key press: {key_char}")
        
        # Create a mock key object
        class MockKey:
            def __init__(self, char):
                self.char = char
        
        mock_key = MockKey(key_char)
        emitter.on_key_press(mock_key)
        time.sleep(0.1)  # Small delay between key presses
    
    print("✓ Keyboard simulation test passed")


def interactive_test():
    """Run interactive test with user input."""
    print("\n" + "="*50)
    print("PhantomStroke Interactive Test")
    print("="*50)
    print("Type some text to test keystroke detection.")
    print("Each character will trigger an ultrasonic tone.")
    print("Type 'quit' to exit.")
    print()
    
    emitter = UltrasonicEmitter(duration=0.1)
    
    try:
        while True:
            user_input = input("Enter text (or 'quit'): ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            print(f"Processing: '{user_input}'")
            for i, char in enumerate(user_input):
                print(f"  [{i+1}] Key: '{char}' -> ", end="", flush=True)
                success = emitter.generate_ultrasonic_tone()
                print("✓" if success else "✗")
                time.sleep(0.1)
            
            print()
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")


def main():
    """Run all tests."""
    print("PhantomStroke Emitter Test Suite")
    print("=" * 40)
    print()
    
    try:
        # Run automated tests
        test_emitter_basic()
        test_emitter_frequency_range()
        test_keyboard_simulation()
        
        print("\n✓ All automated tests passed!")
        
        # Ask if user wants to run interactive test
        if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
            interactive_test()
        else:
            print("\nRun with '--interactive' flag to test user input simulation.")
    
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()