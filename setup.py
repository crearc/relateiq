import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
    'python-dateutil>=1.5',
    'requests>=1.0',
    'simplejson',
]

tests_require = [
    'mock',
    'nose>=1.0',
    'coverage'
]

setup(
    name="relateiq",
    version="0.1",
    author="Tristan Wietsma",
    author_email="",
    url="",
    description="A Python client for RelateIQ",
    packages=["relateiq"],
    long_description=read('README.md'),
    setup_requires=['nose>=1.0'],
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points={
        'relateiq_scripts': [
            'relateiq-cli = relateiq:main',
        ],
    }
)
