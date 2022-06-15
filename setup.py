from setuptools import setup, find_packages

requirements = ['pandas==1.4.2', 'requests==2.27.1', 'numpy==1.22.4']

setup(
    name="pharos",
    version="0.0.1",
    author="Charlie Cone",
    author_email="charliecone624@gmail.com",
    description="A collection of objects and functions to interact with the AlphaVantage api.",\
    url="https://github.com/charliecone624/pharos",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: >= 3.10.0",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)