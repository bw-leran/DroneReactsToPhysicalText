# Drone Reacts to Physical Text
This program utilizes computer vision and an OCR to detect text directly from video being streamed by a Tello drone. It then executes a command based on the text detected in the stream.

## How to Use?
It works best with a printed piece of paper, and does not do so well with handwritten text. Try holding up a printed piece of paper with the text "up", "down","left", or "right". The drone will be able to execute the commands shown to the camera. If multiple commands are presented to the drone, it will only execute the first command that it registers (in order of left to right)  
