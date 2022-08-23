from setuptools import setup, find_packages

"""
Usage:
python setup.py install
"""

setup(
    name = "enums",
    version = "1.0.0",
    packages=find_packages(include=['enums', 'enums.*']),
)