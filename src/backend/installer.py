from gi.repository import GObject
from src.core.package_manager import PackageManager

class PackageInstaller(GObject.GObject):
    __gsignals__ = {
        'info-extracted': (GObject.SIGNAL_RUN_FIRST, None, (object,)),
        'dependencies-checked': (GObject.SIGNAL_RUN_FIRST, None, (object,)),
        'installation-started': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'installation-finished': (GObject.SIGNAL_RUN_FIRST, None, (bool, str))
    }

    def __init__(self):
        GObject.GObject.__init__(self)

    def extract_package_info(self, package_path: str):
        """Extract package metadata and emit signal"""
        info = PackageManager.get_package_info(package_path)
        self.emit('info-extracted', info)

    def check_dependencies(self, package_path: str):
        """Check for missing dependencies and emit signal"""
        missing = PackageManager.check_dependencies(package_path)
        self.emit('dependencies-checked', missing)

    def install_package(self, package_path: str):
        """Install package and emit progress signals"""
        self.emit('installation-started')
        success = PackageManager.install_package(package_path)
        message = "Package installed successfully" if success else "Installation failed"
        self.emit('installation-finished', success, message)