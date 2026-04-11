from setuptools import find_packages, setup

setup(
    name="pylabo",
    packages=find_packages(),
    version="0.2.2",
    description="Python para Laboratorio",
    author="juacc",
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "gspread",
        "matplotlib",
        "PyQt5",
        "PyQt6",
        "numpy",
        "pandas",
        "scipy",
        "pyvisa",
        "pyvisa-py",
    ],
    extras_require={
        "dev": ["pyvisa-sim"],
    },
)
