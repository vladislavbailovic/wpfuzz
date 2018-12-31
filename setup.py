from setuptools import setup, find_packages
import unittest


def test_suite():
    loader = unittest.TestLoader()
    return loader.discover('test', pattern='*.py')

setup(
    name="wpfuzz",
    version="0.1",
    packages=find_packages(),
    scripts=["fuzz", "cli.py"],
    install_requires=[
        "requests"
    ],
    test_suite='setup.test_suite'
)
