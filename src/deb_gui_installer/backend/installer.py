import subprocess
import threading
from gi.repository import GLib

class PackageInstaller:
    def __init__(self, window):
        self.window = window
        self.process = None
        self.cancelled = False

    def install_package(self, package_path):
        """Install a .deb package with progress updates"""
        self.cancelled = False
        self.window.log(f"Installing package: {package_path}")
        
        def run_installation():
            try:
                # Update progress to 10% (preparing)
                GLib.idle_add(self.window.update_progress, 0.1)
                
                # Run dpkg command
                cmd = ["sudo", "dpkg", "-i", package_path]
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                # Monitor progress
                progress = 0.1
                while True:
                    if self.cancelled:
                        self.process.terminate()
                        GLib.idle_add(self.window.log, "Installation cancelled")
                        break
                        
                    return_code = self.process.poll()
                    if return_code is not None:
                        if return_code == 0:
                            GLib.idle_add(self.window.update_progress, 1.0)
                            GLib.idle_add(self.window.log, "Installation completed successfully")
                        else:
                            error = self.process.stderr.read()
                            GLib.idle_add(self.window.log, f"Installation failed: {error}")
                        break
                    
                    # Simulate progress updates (would be real progress in actual implementation)
                    progress = min(progress + 0.05, 0.9)
                    GLib.idle_add(self.window.update_progress, progress)
                    threading.Event().wait(0.5)
                    
            except Exception as e:
                GLib.idle_add(self.window.log, f"Error: {str(e)}")
                
        # Run in background thread
        thread = threading.Thread(target=run_installation)
        thread.daemon = True
        thread.start()

    def cancel_installation(self):
        """Cancel ongoing installation"""
        self.cancelled = True
        if self.process:
            self.process.terminate()