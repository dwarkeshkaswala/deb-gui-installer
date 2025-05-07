from setuptools import setup, find_packages

setup(
    name="deb-gui-installer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'PyGObject>=3.44.1',
    ],
    entry_points={
        'console_scripts': [
            'deb-installer=src.main:main',
        ],
    },
    python_requires='>=3.6',
)