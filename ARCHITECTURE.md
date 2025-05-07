# Debian Package Installer Architecture

## Overview
A GUI application for installing .deb packages on Debian-based systems (like Kali Linux) with dependency resolution.

## Components

### 1. Main Application (`src/main.py`)
- Entry point of the application
- Initializes GTK and creates the main window
- Manages the application lifecycle

### 2. UI Components (`src/ui/`)
- `main_window.py`: Main application window with package selection and status display
- `package_view.py`: (Future) Detailed package information view

### 3. Core Logic (`src/core/`)
- `package_manager.py`: Handles package installation and dependency management
  - Uses `dpkg` for package operations
  - Uses `apt` for dependency resolution

### 4. Backend Services (`src/backend/`)
- `installer.py`: (Future) Installation progress tracking and error handling

## Technical Stack
- Python 3
- GTK 3 for GUI
- Subprocess for system commands (`dpkg`, `apt`)
- Standard Linux tools for package management

## Installation Flow
1. User selects .deb file
2. Application extracts package metadata
3. Checks for missing dependencies
4. Installs package with dependencies
5. Shows installation status

## Future Enhancements
- Batch installation of multiple packages
- Repository integration
- Advanced dependency visualization
- Dark mode support