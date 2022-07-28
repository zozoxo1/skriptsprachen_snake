from setuptools import setup, find_packages

setup(
    name = "enums",
    version = "1.0.0",
    packages=find_packages(include=['enums', 'enums.*']),
)