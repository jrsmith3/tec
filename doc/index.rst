.. tec documentation master file, created by
   sphinx-quickstart on Wed Feb 27 21:44:45 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


tec - Utils for simulating vacuum thermionic energy conversion devices
======================================================================
The tec package provides a uniform and extensible API for easily simulating thermionic energy conversion devices (TECs). A few models are supplied with the tec package, but others can be easily added.

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


Quickstart
==========
TEC models are built by subclassing the TECBase class and adding functionality to calculate the motive. As a quick example, say the user wanted to simulate the device described in Hatsopoulous and Gyftopoulous :cite:`978-0-26-208059-0`

   >>> # Pull in Langmuir's model.
   >>> from tec.models import Langmuir

   >>> # Create a dict containing the emitter parameters (assume emissivity = 0.5).
   >>> em = {"temp":1,
         "barrier":1,
         "voltage":1,
         "position":0,
         "richardson":10,
         "emissivity":0.5}

   >>> # Create the collector parameters.
   >>> em = {"temp":1,
   >>>       "barrier":1,
   >>>       "voltage":1,
   >>>       "position":0,
   >>>       "richardson":10,
   >>>       "emissivity":0.5}

   >>> # Put everything together to instantiate the TEC.
   >>> tec_params = {"Emitter":em, "Collector":co}
   >>> T = Langmuir(tec_params)

   >>> # What's the maximum output power density of this thing?
   >>> T.calc_output_power_density(with_output="max")

   >>> # What if we want to know the output power density if the device
   >>> # is operating at maximum efficiency? First, calculate the maximum
   >>> # efficiency and set the TEC to the corresponding voltage.
   >>> T.calc_total_efficiency(with_output="max",set_voltage=True)

   >>> # And look, the output voltage was set such that the TEC is at max efficiency.
   >>> T.calc_output_voltage()

   >>> # Now let's calculate the value of maximum output power.
   >>> T.calc_output_power_density()

   >>> # What does the motive diagram at this voltage look like?
   >>> T.plot_motive()

   >>> # Looks like a lot of negative space charge. What if we decrease the 
   >>> # interelectrode spacing?
   >>> T["Collector"]["position"] = 5
   >>> T.calc_total_efficiency(with_output="max",set_voltage=True)
   >>> T.calc_output_power_density()
   >>> T.plot_motive()


Reference
=========

.. toctree::
   	:maxdepth: 2

   	api
   	models


Bibliography
============
.. bibliography:: bib.bib
