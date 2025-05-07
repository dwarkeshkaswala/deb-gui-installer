import subprocess
import re
from typing import Optional, Dict, List

class PackageManager:
    @staticmethod
    def get_package_info(package_path: str) -> Optional[Dict[str, str]]:
        """Extract package metadata from .deb file"""
        try:
            result = subprocess.run(
                ['dpkg', '-I', package_path],
                capture_output=True,
                text=True,
                check=True
            )
            return PackageManager._parse_dpkg_output(result.stdout)
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def _parse_dpkg_output(output: str) -> Dict[str, str]:
        """Parse dpkg output into structured data"""
        info = {}
        patterns = {
            'Package': r'Package:\s*(.+)',
            'Version': r'Version:\s*(.+)',
            'Architecture': r'Architecture:\s*(.+)',
            'Maintainer': r'Maintainer:\s*(.+)',
            'Description': r'Description:\s*(.+)',
            'Depends': r'Depends:\s*(.+)'
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, output)
            if match:
                info[key] = match.group(1).strip()

        return info

    @staticmethod
    def install_package(package_path: str) -> bool:
        """Install the .deb package using dpkg"""
        try:
            subprocess.run(
                ['sudo', 'dpkg', '-i', package_path],
                check=True
            )
            # Fix any missing dependencies
            subprocess.run(
                ['sudo', 'apt-get', 'install', '-f'],
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def check_dependencies(package_path: str) -> List[str]:
        """Check for missing dependencies"""
        info = PackageManager.get_package_info(package_path)
        if not info or 'Depends' not in info:
            return []

        depends = info['Depends'].split(',')
        missing = []
        for dep in depends:
            dep = dep.strip().split(' ')[0]  # Remove version constraints
            try:
                subprocess.run(
                    ['dpkg', '-s', dep],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except subprocess.CalledProcessError:
                missing.append(dep)

        return missing