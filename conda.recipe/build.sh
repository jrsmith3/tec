#!/usr/bin/env bash

# Define version from `tec/version.py`
VERSION=`python -c 'execfile("tec/version.py")
print(__version__)'`

echo $VERSION > __conda_version__.txt

# Install package
$PYTHON setup.py install
