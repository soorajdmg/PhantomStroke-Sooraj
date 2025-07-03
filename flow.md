```mermaid
flowchart LR
    %% Laptop (Transmitter)
    subgraph Laptop_Transmitter
        A1[User types on keyboard]
        A2[Each keystroke triggers ultrasonic emission at MEMS resonance frequency]
        A3[Emits ultrasonic wave (18-22 kHz)]
    end

    %% Smartphone (Receiver)
    subgraph Smartphone_Receiver
        B1[Malicious web page running]
        B2[Has gyroscope access via JavaScript (Sensor API)]
        B3[MEMS gyroscope picks up tiny internal oscillation]
        B4[Gyroscope output distorted]
        B5[Output read by JS page]
        B6[Bitstream decoded from vibration pattern]
    end

    %% Flow connections
    A1 --> A2 --> A3 --> B3
    B1 --> B2 --> B3
    B3 --> B4 --> B5 --> B6
```
