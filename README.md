# Interactive Drawing with Arduino
This project leverages a combination of computer vision and hardware interface technologies to create an interactive drawing application that responds to hand gestures captured via a webcam. Users can draw on their computer screen by moving their hands in the air and the application can recognize simple geometric shapes drawn by the user. Furthermore, based on the type of shape drawn, the program can interact with an Arduino-controlled LED, turning it on or off. Below is a detailed description of the system, its components, and functionalities:

### 1. System Overview
The core of this project integrates:
- **OpenCV**: For image processing and drawing interface.
- **MediaPipe**: For real-time hand tracking using a machine learning model.
- **pyFirmata**: For communicating with an Arduino board to control external devices like LEDs.
- **Python**: As the programming language tying all components together.

### 2. Functional Components
#### a. Hand Tracking
Using MediaPipe’s hand tracking capabilities, the program captures live video from a webcam and detects the position of the user's hand and fingers in real-time. Specifically, it identifies landmarks on a single hand, focusing on the tips of the index finger and thumb for gesture recognition.

#### b. Drawing Mechanism
The user can draw on a virtual canvas displayed on their computer screen. Movement of the index finger in the air translates to drawing paths on the canvas, while touching the thumb to the index finger acts as a toggle to stop/start drawing. This toggling is detected using the Euclidean distance between the two finger tips, checking if they are within a specific close range.

#### c. User Interface
- **Clear Button**: A designated area on the frame serves as a "clear" button. If the user's index finger hovers over this area and is recognized by the program, the canvas is cleared of all drawings.
- **Live Feedback**: The user sees a real-time video feed with hand landmarks drawn, providing visual feedback of hand positioning and what the system is tracking.

#### d. Shape Recognition
When the user stops drawing (detected by the touching of thumb and index finger), the application automatically analyzes the points drawn to classify the shape. This is done using contour analysis and polygon approximation to differentiate between basic shapes like triangles, rectangles, squares, and circles.

#### e. Arduino Interaction
Depending on the shape recognized, the program sends a command to an Arduino board:
- If a circle is detected, the program sends a signal to turn on an LED connected to pin 13 on the Arduino.
- For any other shape, the LED is turned off.
This interaction serves as a simple demonstration of how physical computing can be integrated with computer vision.

### 3. Use Cases
This application can serve educational purposes for teaching concepts of computer vision, machine learning, and basic electronics. It could also be extended or modified for more interactive and engaging user experiences in installations, educational tools, or creative design processes.

### 4. Extensions and Improvements
- **Increased Shape Diversity**: Adding more complex shape recognition for enhanced interaction.
- **Multi-Hand Support**: Expanding the system to track and differentiate actions from two hands.
- **Gesture Customization**: Allowing users to define their own gestures and corresponding responses.
- **Improved UX/UI**: Creating a more polished user interface with intuitive controls and feedback.

### 5. Challenges and Considerations
- **Lighting and Background Noise**: The system's performance in different lighting conditions and backgrounds can affect accuracy.
- **Real-Time Processing Demands**: Ensuring the system remains responsive and accurate in real-time without significant lags.

Overall, this project combines advanced technologies in a creative way to build an interactive system that bridges the gap between digital and physical computing worlds.
