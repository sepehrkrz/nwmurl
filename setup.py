from setuptools import setup, find_packages

# Provide the long description directly with RST markup
LONG_DESCRIPTION = """
=======================
nwmurl
=======================

URL generator tool for National Water Model data

Overview
--------

`nwmurl` is a Python package that allows you to generate URLs for National Water Model (NWM) data.

Usage
-----

Install the package using pip:

.. code-block:: bash

    pip install nwmurl

Then, you can use it in your Python code:

.. code-block:: python

    from nwmurl import generate_url

    url = generate_url(model="short_range", comid=12345, datetime="2023-10-29T12:00:00Z")

"""

# Other information
VERSION = '0.1.4'
DESCRIPTION = 'URL generator tool for National Water Model data'

setup(
    name="nwmurl",
    version=VERSION,
    author="Sepehr Karimi (CIROH)",
    author_email="mkarimiziarani@ua.edu",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
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
