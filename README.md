# Perfect Casting

This script automates the process of casting a rod in the game Roblox, ensuring that every cast is perfect.

## Description

The `perfect_casting.py` script captures the screen, detects specific colors (green and white), and simulates mouse actions to automate perfect rod casting in Roblox. The script uses OpenCV for image processing, MSS for screen capturing, and PyAutoGUI for simulating mouse actions.

## Example Video

Watch the script in action:

[![Perfect Casting Example](http://img.youtube.com/vi/o2rAoz3OoKs/0.jpg)](http://www.youtube.com/watch?v=o2rAoz3OoKs)

## Installation

1. Clone the repository or download the script.
2. Install the required dependencies using pip:

    ```sh
    pip install opencv-python-headless numpy mss pygetwindow pyautogui
    ```

## Usage

1. Ensure that the Roblox game window is open and the title of the window is "Roblox".
2. **It is recommended to go to camera mode first and avoid equipping any green titles, as they can affect how the computer vision works.**
3. **To ensure the best vision for the script, make sure to limit the green space in the screen to the green box when casting.**
4. Run the script:

    ```sh
    python perfect_casting.py
    ```

5. The script will continuously capture the screen, detect the necessary colors, and simulate mouse actions to ensure perfect casting.

## Configuration

- `CONFIG_BOUNDING_TOP`: Adjust the top boundary for screen capture.