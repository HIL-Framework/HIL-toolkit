from setuptools import setup, find_packages

setup(
    name="HIL",
    version="0.1.0",
    packages=find_packages(include=["HIL", "HIL.optimization.*"])
)