.. tec documentation master file, created by
   sphinx-quickstart on Wed Feb 27 21:44:45 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

tec - Utils for simulating vacuum thermionic energy conversion devices
======================================================================
The purpose of this package is to make simulating the performance of thermionic energy conversion devices easy. To this end, the tec package provides several features:
  
* An API that provides the user with the functionality they want without requiring them to wade into the arcane details of the calculations.
* A modular structure so that new algorithms can be implemented with the same API.
* A small library of known algorithms for calculating device performance.
* Numerical tests implemented as unit tests to provide some assurance of numerical accuracy.
* A system for generating and recording general sets of data so that the most time consuming part of the calculation need only be run once.
* Descriptive documentation.
  
There are three major components to this package: the library, the scripting system, and the testing system.


Installation
============

Prerequisites
-------------
The :mod:`tec` module is implemented in python and depends on `numpy <http://www.numpy.org>`_, `scipy <http://www.scipy.org>`_, and `matplotlib <http://matplotlib.org>`_. It isn't required, but I recommend installing `ipython <http://ipython.org>`_ as well. These packages and more are available via Continuum Analytics's `anaconda <http://continuum.io/downloads>`_ distribution. Anaconda is likely the quickest way to get set up with the prerequisites.

If you are on windows, let me know how you install this stuff because I don't have access to a windows box. Hit me up on the `issue tracker <https://github.com/jrsmith3/tec/issues?state=open>`_ if you have suggestions for windows.

tec installation
----------------
The code isn't on pypi, so you'll have to install from source. There are two ways to do it: 1. downloading and installing from the zip file and 2. installing with pip over git from github. If you don't understand the phrase, "installing over git from github", you want to use the first option.

Zip file install
----------------
All you have to do is download the most recent version (0.3.2) from the internet `here <https://github.com/jrsmith3/tec/archive/0.3.2.zip>`_. Unzip the file and switch into the directory into which the zip file was uncompressed. Then execute the following command at the command line.

    $ python setup.py install

pip + git + github
------------------
If you have pip installed, things should be pretty easy. Just execute

    $ pip install git+git://github.com/jrsmith3/tec.git

.. toctree::
   	:maxdepth: 2

   	Quickstart <quickstart>
   	Library <library>
   	Scripting <scripting>
   	Testing <testing>

Reference
---------

.. toctree::
   	:maxdepth: 2

   	api
   	models
   	Testing numerical accuracy of models <numerics>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

