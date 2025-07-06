# PhantomStroke

A proof-of-concept implementation of an acoustic side-channel attack that uses ultrasonic tones to potentially interfere with MEMS gyroscopes in smartphones.

## ⚠️ Security Research Disclaimer

This project is for **academic research and security awareness purposes only**. It demonstrates potential vulnerabilities in sensor systems and should not be used for malicious purposes.

## Overview

PhantomStroke implements a multi-phase attack where a compromised laptop emits ultrasonic tones (18-22 kHz) triggered by keystrokes, potentially causing interference with nearby smartphone gyroscopes.

### Attack Phases

1. **Phase 1: Ultrasonic Emission (This Implementation)**
   - Detect keystrokes in real-time
   - Emit ultrasonic tones (18-22 kHz) for each keystroke
   - Target the resonance frequency of MEMS gyroscope structures

2. **Phase 2-5: Smartphone Reception & Processing** (Future Work)
   - JavaScript-based gyroscope monitoring
   - Signal processing and ML-based keystroke inference

## Installation

### Dependencies

The emitter supports multiple audio and keyboard backends with graceful fallback:

```bash
# Recommended (high-quality audio)
pip install sounddevice numpy pynput

# Alternative audio backend
pip install pyaudio pynput

# Fallback mode (simulation only)
# No dependencies required - uses built-in libraries
```

### Quick Install

```bash
git clone https://github.com/Soorya005/PhantomStroke.git
cd PhantomStroke
pip install -r requirements.txt
```

## Usage

### Basic Keystroke Monitoring

```bash
# Start real-time keystroke monitoring with ultrasonic emission
python3 emitter.py

# Test tone generation without keyboard monitoring
python3 emitter.py --test
```

### Testing

```bash
# Run automated tests
python3 test_emitter.py

# Run interactive simulation
python3 test_emitter.py --interactive
```

### Programmatic Usage

```python
from emitter import UltrasonicEmitter

# Create emitter with custom settings
emitter = UltrasonicEmitter(
    frequency_range=(18000, 22000),  # Hz
    duration=0.1,                    # seconds
    volume=0.7,                      # 0.0 to 1.0
    sample_rate=44100               # Hz
)

# Test single tone
emitter.generate_ultrasonic_tone(20000)  # 20 kHz

# Start keyboard monitoring
emitter.start_monitoring()
```

## Configuration

### Frequency Range
- **Default**: 18-22 kHz (ultrasonic range)
- **Target**: MEMS gyroscope resonance frequencies
- **Configurable**: Adjust based on target device specifications

### Audio Backends
1. **sounddevice + numpy**: High-quality, low-latency audio
2. **pyaudio**: Alternative audio library
3. **fallback**: Simulation mode (no actual audio output)

### Keyboard Backends
1. **pynput**: Cross-platform keyboard monitoring
2. **keyboard**: Alternative keyboard library  
3. **fallback**: Manual input simulation

## Technical Details

### Ultrasonic Frequency Selection
- **18-22 kHz**: Above human hearing range (~20 Hz to 20 kHz)
- **MEMS Resonance**: Targets typical gyroscope resonance frequencies
- **Random Variation**: Each keystroke uses a random frequency within range

### Attack Vector
- **Physical**: Acoustic coupling through air
- **Target**: MEMS gyroscope internal vibrating structures
- **Effect**: False angular velocity readings
- **Range**: Typically effective within 1-2 meters

## Project Structure

```
PhantomStroke/
├── emitter.py          # Main ultrasonic emitter implementation
├── test_emitter.py     # Test suite and interactive demos
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── flowchart.md       # Attack flow documentation
├── flow.md            # Simplified flow diagram
└── LICENSE            # Academic research license
```

## Testing Results

The implementation has been tested with:
- ✅ Ultrasonic tone generation (18-22 kHz)
- ✅ Real-time keystroke detection
- ✅ Frequency randomization
- ✅ Multiple audio/keyboard backends
- ✅ Graceful fallback modes
- ✅ Cross-platform compatibility

## Future Work

1. **Smartphone Receiver** (Phase 2-5)
   - JavaScript gyroscope API integration
   - Real-time signal processing
   - Machine learning keystroke classification

2. **Attack Optimization**
   - Frequency tuning for specific device models
   - Signal strength optimization
   - Anti-detection techniques

3. **Defense Mechanisms**
   - Gyroscope noise filtering
   - Anomaly detection
   - Rate limiting

## Research Context

This implementation is based on research into:
- MEMS sensor vulnerabilities
- Acoustic side-channel attacks
- Sensor fusion security
- Smartphone privacy implications

## Ethical Usage

This tool is intended for:
- ✅ Security research and education
- ✅ Vulnerability assessment
- ✅ Academic studies
- ❌ Unauthorized surveillance
- ❌ Privacy violation
- ❌ Malicious attacks

## License

Academic and research use only. See LICENSE file for details.

## Contributors

- @Soorya005 - Lead Developer
- Vyshnav Pradeep - Research Contributor  
- Sooraj - Research Contributor