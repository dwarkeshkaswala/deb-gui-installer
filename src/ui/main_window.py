import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from src.backend.installer import PackageInstaller

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Debian Package Installer")
        self.set_default_size(800, 600)
        self.set_border_width(10)
        
        # Initialize installer
        self.installer = PackageInstaller()
        self._connect_signals()
        
        # Main container
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)
        
        # Header
        self.header = Gtk.HeaderBar(title="Debian Package Installer")
        self.header.set_subtitle("Install .deb packages with ease")
        self.header.set_show_close_button(True)
        self.set_titlebar(self.header)
        
        # Package selection area
        self.create_package_selection()
        
        # Install button
        self.install_btn = Gtk.Button(label="Install Package")
        self.install_btn.set_sensitive(False)
        self.install_btn.connect("clicked", self.on_install_clicked)
        self.box.pack_start(self.install_btn, False, False, 0)
        
        # Status bar
        self.create_status_bar()
        
    def _connect_signals(self):
        self.installer.connect('info-extracted', self.on_info_extracted)
        self.installer.connect('dependencies-checked', self.on_dependencies_checked)
        self.installer.connect('installation-finished', self.on_installation_finished)
        
    def create_package_selection(self):
        frame = Gtk.Frame(label="Package Selection")
        self.box.pack_start(frame, True, True, 0)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        frame.add(vbox)
        
        # File chooser button
        self.file_btn = Gtk.FileChooserButton(title="Select .deb package")
        self.file_btn.set_action(Gtk.FileChooserAction.OPEN)
        filter_deb = Gtk.FileFilter()
        filter_deb.set_name("Debian packages")
        filter_deb.add_pattern("*.deb")
        self.file_btn.add_filter(filter_deb)
        self.file_btn.connect("file-set", self.on_file_selected)
        vbox.pack_start(self.file_btn, False, False, 0)
        
        # Package info area
        self.info_label = Gtk.Label(label="No package selected")
        vbox.pack_start(self.info_label, True, True, 0)
        
    def create_status_bar(self):
        self.status_bar = Gtk.Statusbar()
        self.box.pack_end(self.status_bar, False, False, 0)
        
    def on_file_selected(self, widget):
        package_path = widget.get_filename()
        self.installer.extract_package_info(package_path)
        
    def on_info_extracted(self, installer, info):
        if info:
            text = f"Package: {info.get('Package', 'N/A')}\n"
            text += f"Version: {info.get('Version', 'N/A')}\n"
            text += f"Description: {info.get('Description', 'N/A')}"
            self.info_label.set_text(text)
            self.install_btn.set_sensitive(True)
            self.installer.check_dependencies(self.file_btn.get_filename())
        else:
            self.info_label.set_text("Invalid package file")
            self.install_btn.set_sensitive(False)
            
    def on_dependencies_checked(self, installer, missing):
        if missing:
            self.status_bar.push(0, f"Missing dependencies: {', '.join(missing)}")
        else:
            self.status_bar.push(0, "All dependencies are satisfied")
            
    def on_install_clicked(self, widget):
        package_path = self.file_btn.get_filename()
        self.installer.install_package(package_path)
        
    def on_installation_finished(self, installer, success, message):
        self.status_bar.push(0, message)
        if success:
            self.info_label.set_text("Installation complete!")