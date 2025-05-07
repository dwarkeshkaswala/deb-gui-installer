import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from deb_gui_installer.backend.installer import PackageInstaller

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Debian Package Installer")
        self.set_default_size(800, 600)
        
        self.installer = PackageInstaller(self)
        self.current_package = None
        
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)
        
        self.package_frame = Gtk.Frame(label="Package Selection")
        self.package_box = Gtk.Box(spacing=6)
        self.package_frame.add(self.package_box)
        self.box.pack_start(self.package_frame, False, False, 0)
        
        self.package_label = Gtk.Label(label="No package selected")
        self.package_box.pack_start(self.package_label, True, True, 0)
        
        self.browse_button = Gtk.Button(label="Browse...")
        self.browse_button.connect("clicked", self.on_browse_clicked)
        self.package_box.pack_start(self.browse_button, False, False, 0)
        
        self.progress = Gtk.ProgressBar()
        self.box.pack_start(self.progress, False, False, 0)
        
        self.log_frame = Gtk.Frame(label="Installation Log")
        self.log_view = Gtk.TextView()
        self.log_view.set_editable(False)
        self.log_view.set_wrap_mode(Gtk.WrapMode.WORD)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.log_view)
        self.log_frame.add(scrolled_window)
        self.box.pack_start(self.log_frame, True, True, 0)
        
        self.button_box = Gtk.Box(spacing=6)
        self.box.pack_start(self.button_box, False, False, 0)
        
        self.install_button = Gtk.Button(label="Install")
        self.install_button.set_sensitive(False)
        self.button_box.pack_start(self.install_button, True, True, 0)
        
        self.cancel_button = Gtk.Button(label="Cancel")
        self.button_box.pack_start(self.cancel_button, True, True, 0)
        
        self.install_button.connect("clicked", self.on_install_clicked)
        self.cancel_button.connect("clicked", self.on_cancel_clicked)
        
    def on_browse_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Select Debian Package",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        filter_deb = Gtk.FileFilter()
        filter_deb.set_name("Debian packages")
        filter_deb.add_pattern("*.deb")
        dialog.add_filter(filter_deb)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.current_package = dialog.get_filename()
            self.package_label.set_text(self.current_package)
            self.install_button.set_sensitive(True)
            self.log(f"Selected package: {self.current_package}")
        
        dialog.destroy()
        
    def on_install_clicked(self, button):
        if self.current_package:
            self.installer.install_package(self.current_package)
        
    def on_cancel_clicked(self, button):
        self.installer.cancel_installation()
        
    def log(self, message):
        buffer = self.log_view.get_buffer()
        end_iter = buffer.get_end_iter()
        buffer.insert(end_iter, message + "\n")
        mark = buffer.create_mark(None, end_iter, False)
        self.log_view.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)
        
    def update_progress(self, fraction):
        self.progress.set_fraction(fraction)
        self.progress.set_text(f"{int(fraction * 100)}%")