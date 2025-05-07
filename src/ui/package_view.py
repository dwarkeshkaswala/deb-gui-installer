import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class PackageView(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        # Package info labels
        self.name_label = Gtk.Label(label="<b>Package:</b> ", use_markup=True, xalign=0)
        self.version_label = Gtk.Label(label="<b>Version:</b> ", use_markup=True, xalign=0)
        self.arch_label = Gtk.Label(label="<b>Architecture:</b> ", use_markup=True, xalign=0)
        self.desc_label = Gtk.Label(label="<b>Description:</b> ", use_markup=True, xalign=0)
        self.deps_label = Gtk.Label(label="<b>Dependencies:</b> ", use_markup=True, xalign=0)
        
        # Add labels to the box
        self.pack_start(self.name_label, False, False, 0)
        self.pack_start(self.version_label, False, False, 0)
        self.pack_start(self.arch_label, False, False, 0)
        self.pack_start(self.desc_label, False, False, 0)
        self.pack_start(self.deps_label, False, False, 0)
        
        # Dependency tree view
        self.deps_tree = Gtk.TreeView()
        self.deps_model = Gtk.ListStore(str, str, str)  # Name, Version, Status
        self.deps_tree.set_model(self.deps_model)
        
        # Add columns
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Dependency", renderer, text=0)
        self.deps_tree.append_column(column)
        
        column = Gtk.TreeViewColumn("Version", renderer, text=1)
        self.deps_tree.append_column(column)
        
        column = Gtk.TreeViewColumn("Status", renderer, text=2)
        self.deps_tree.append_column(column)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.add(self.deps_tree)
        self.pack_start(scrolled, True, True, 0)
    
    def update_package_info(self, package_info: dict):
        """Update the view with package information"""
        self.name_label.set_text(f"<b>Package:</b> {package_info.get('name', 'N/A')}")
        self.version_label.set_text(f"<b>Version:</b> {package_info.get('version', 'N/A')}")
        self.arch_label.set_text(f"<b>Architecture:</b> {package_info.get('architecture', 'N/A')}")
        self.desc_label.set_text(f"<b>Description:</b> {package_info.get('description', 'N/A')}")
        
        # Update dependencies
        self.deps_model.clear()
        for dep in package_info.get('dependencies', []):
            self.deps_model.append([
                dep.get('name', 'N/A'),
                dep.get('version', 'N/A'),
                dep.get('status', 'Not installed')
            ])