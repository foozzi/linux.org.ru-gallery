import os
from setuptools import setup, find_packages


base_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base_path, 'requirements.txt'), 'r') as f:
    requirements = f.read().split('\n')

with open(os.path.join(base_path, 'README.md'), 'r') as f:
    description = f.read()

setup(
    name='lorgallery',
    version='1.1',
    packages=find_packages(),
    install_requires=requirements,
    long_description=description,
)
