# Debian Package GUI Installer

A professional, open-source GUI application for installing .deb packages on Debian-based Linux distributions.

## Features

- Simple graphical interface for .deb package installation
- Package metadata extraction (name, version, description)
- Dependency checking and automatic resolution
- Native GTK3 interface for Linux systems
- Supports Kali Linux and other Debian-based distros

## Requirements

- Python 3.6+
- GTK 3.0 development libraries
- dpkg and apt utilities (standard on Debian systems)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/deb-gui-installer.git
cd deb-gui-installer
```

2. Install system dependencies:
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

3. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python src/main.py
```

## Screenshot

![Application Screenshot](screenshot.png)

## Contributing

Contributions are welcome! Please open an issue or pull request.

## License

MIT License - See LICENSE file for details
