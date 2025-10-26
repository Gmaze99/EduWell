from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requiremnts = f.read().splitlines()

setup(
    name="EduWellness",
    version="0.1.0",
    author="Ashish Sharma",
    packages=find_packages(),
    install_requires=requiremnts,
)
