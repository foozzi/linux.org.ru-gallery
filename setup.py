from setuptools import setup, find_packages
from os.path import join, dirname
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)

reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='lorgallery',
    version='1.1',
    packages=find_packages(),
    install_requires=reqs,
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    scripts=['bin/lorgallery'],
    )
