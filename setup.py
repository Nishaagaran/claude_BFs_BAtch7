from setuptools import setup, find_packages

setup(
    name="patient-health-analyser",
    version="0.1.0",
    description="A Python project for analyzing patient health data",
    author="Your Name",
    author_email="your.email@example.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[],
)
