from setuptools import setup, find_packages

setup(
    name="wpfuzz",
    version="0.1",
    packages=find_packages(),
    scripts=["fuzz", "cli.py"],
    install_requires=[
        "requests"
    ]
)
