#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from .ui.main_window import MainWindow

class DebInstallerApp:
    def __init__(self):
        self.window = MainWindow()
        
    def run(self):
        self.window.show_all()
        Gtk.main()

def main():
    app = DebInstallerApp()
    app.run()

if __name__ == "__main__":
    main()