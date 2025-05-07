from deb_gui_installer.ui.main_window import MainWindow
from gi.repository import Gtk

def main():
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()