# Discord Custom Activity

Discord Custom Activity is a Python application that allows you to set a custom activity status on your Discord profile. This application uses the Discord Rich Presence API to update your status with custom text, and images. mb iam still new using python 

## Features

- Set custom activity type (Playing, Listening to, Watching)
- Customizable activity text and description
- Add large and small images with descriptions
- button
- Option to include a timestamp
- Save and load configuration
- Minimize to system tray

## Requirements

- Python 3.6+
- `tkinter` (usually included with Python)
- `pypresence`
- `Pillow`
- `pystray`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ItzApipAjalah/py-discordrpc.git
    cd discord-custom-activity
    ```

2. Install the required Python packages:
    ```sh
    pip install pypresence Pillow pystray
    ```

## Usage

1. Run the application:
    ```sh
    python index.py
    ```

2. Enter your Discord application client ID when prompted.

3. Customize your activity status using the GUI.

4. Click "Set Activity" to update your Discord status.

5. Optionally, click "Hide to Tray" to minimize the application to the system tray.

## Configuration

The application saves your configuration to a JSON file located in your AppData directory (`%APPDATA%/discord_custom_activity_config.json`). The configuration is automatically loaded when you start the application.

## Screenshots

![Main Window](https://raw.githubusercontent.com/ItzApipAjalah/nodejs-embedanimstream/refs/heads/main/main.png)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [pypresence](https://github.com/qwertyquerty/pypresence) - A library for Discord Rich Presence
- [Pillow](https://python-pillow.org/) - Python Imaging Library
- [pystray](https://github.com/moses-palmer/pystray) - Cross-platform system tray icon

