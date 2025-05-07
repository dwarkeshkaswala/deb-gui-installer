from setuptools import setup, find_packages

setup(
    name="deb-gui-installer",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyGObject",
    ],
    entry_points={
        "console_scripts": [
            "deb-installer=deb_gui_installer.main:main",
        ],
    },
    python_requires=">=3.6",
)