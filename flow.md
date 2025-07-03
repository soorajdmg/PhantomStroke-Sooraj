```mermaid
flowchart LR
    subgraph Laptop_Transmitter [Laptop (Transmitter)]
        A1[User types on keyboard]
        A2[Each keystroke triggers\nultrasonic emission\nat MEMS resonance frequency]
        A3[Emits ultrasonic wave (18–22 kHz)]
    end

    subgraph Smartphone_Receiver [Smartphone (Receiver)]
        B1[Malicious web page running]
        B2[Has gyroscope access via\nJavaScript (Sensor API)]
        B3[MEMS gyroscope picks up\ntiny internal oscillation]
        B4[Gyroscope output distorted]
        B5[Output read by JS page]
        B6[Bitstream decoded from\nvibration pattern]
    end

    A1 --> A2 --> A3 --> B3
    B1 --> B2 --> B3
    B3 --> B4 --> B5 --> B6
```
