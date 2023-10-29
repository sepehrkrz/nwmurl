from setuptools import setup, find_packages
import os


VERSION = '0.1.0'
DESCRIPTION = 'URL generator tool for National Water Model data'
LONG_DESCRIPTION = 'A package that allows to generate urls for NWM data.'

# Setting up
setup(
    name="nwmurl",
    version=VERSION,
    author="Sepehr Karimi (CIROH)",
    author_email="<mkarimiziarani@ua.edu>",
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'NWM', 'url'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
