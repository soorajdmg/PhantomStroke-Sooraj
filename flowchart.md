```mermaid
flowchart TD
    %% Phase 1: Attack Trigger
    A1[User Types on Laptop Keyboard]
    A2[Each Keystroke Triggers Ultrasonic Signal\n(18-22 kHz)]
    A3[Ultrasonic Signal Emitted via Laptop Speaker]

    %% Phase 2: Signal Reception on Phone
    B1[Smartphone Nearby with Malicious Web Page Open]
    B2[JavaScript Checks for Gyroscope API Support]
    B3{Is 'Gyroscope' in window?}
    B4[Use Generic Sensor API (High Precision)]
    B5[Fallback to DeviceOrientationEvent (Low Precision)]

    %% Phase 3: Sensor Reading
    C1[Gyroscope Reads Internal MEMS Vibrations]
    C2[Time-Series X, Y, Z Angular Velocity Captured]
    C3[Buffer & Segment Signal into Windows]

    %% Phase 4: Optional Server Use
    D1{Send Data to Server or Process Locally?}
    D2[Send Buffered Data to Remote Server\n(Requires API Key)]
    D3[Process Locally using ML In-Browser]

    %% Phase 5: ML Inference
    E1[Feature Extraction (FFT, Axis Stats)]
    E2[ML Model (e.g., CNN/SVM) Predicts Keystroke]
    E3[Output Inferred Keystrokes]

    %% Connections
    A1 --> A2 --> A3 --> B1
    B1 --> B2 --> B3
    B3 -- Yes --> B4 --> C1
    B3 -- No  --> B5 --> C1
    C1 --> C2 --> C3 --> D1
    D1 -- Remote --> D2 --> E1
    D1 -- Local  --> D3 --> E1
    E1 --> E2 --> E3
```
