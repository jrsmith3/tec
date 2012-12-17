tec - A python package for simulating vacuum thermionic energy conversion devices.

The purpose of this package is to make simulating the performance of thermionic energy conversion devices easy. To this end, the tec package provides several features:
  
  * An API that provides the user with the functionality they want without requiring them to wade into the arcane details of the calculations.
  * A modular structure so that new algorithms can be implemented with the same API.
  * A small library of known algorithms for calculating device performance.
  * Numerical tests implemented as unit tests to provide some assurance of numerical accuracy.
  * A system for generating and recording general sets of data so that the most time consuming part of the calculation need only be run once.
  * Descriptive documentation.
  
There are three major components to this package: the library, the scripting system, and the testing system.


Library
=======
At the heart of the tec package is the TEC class. This class implements the functionality of a thermionic energy conversion device. To simulate the performance of a TEC, the user instantiates a TEC object and calls methods to acquire data about its present state (e.g. output power density, efficiency, etc.). The following paragraphs describe the general features of the TEC class; see the class documentation for the specifics.

There are many different models of electron transport through a TEC. A major objective of the TEC class is to provide a generic interface for the user without requiring the user to understand the arcane specificities of the particular model. The TEC class is written so that it can be subclassed in order to implement an arbitrary model.

The question at the heart of all models of electron transport across a TEC is: how is the electron motive calculated? Therefore, the TEC class and any subclass essentially addresses that question. The TEC class is instantiated with data describing its state. A call to a method of the TEC class results in the calculation of the electron motive and any associated model-dependent metadata. Acquiring this data and metadata is generally the most computationally intensive calculation that must be performed and so it is calculated only once and stored in the TEC object for subsequent calculations. If the data of the TEC object is modified so as to change the motive, the motive data and metadata of the TEC object is deleted and new motive data and metadata are calculated. The TEC class provides methods to retrieve the data and metadata associated with the calculation of the motive. The nature of this data and metadata may vary depending on the specifics of the model. The TEC class and any subclass has a description of the algorithm used to calculate the motive as well as a description of the data and metadata generated during the calculation of the motive.

The TEC class treats its data similar to a python dictionary. TEC objects have two data fields: Emitter and Collector. The data of each field is an Electrode object. The data for each electrode of the TEC is enough to fully specify the state of the TEC object. As mentioned previously, the TEC class provides methods to return values of interest to the user such as output power density, Carnot efficiency, or back current density.

The TEC parent class implements the most basic model: it ignores the negative space charge effect and calculates a linear motive between the emitter vacuum level and collector vacuum level.


Scripting System
================
The classes and API of the tec package's library were designed to create a generic interface separate from the implementation details of any particular model. While this design is useful, it doesn't completely address all of the requirements a user has. For example, many times a user is interested in seeing the output power density vs. voltage of a device who's other parameters remain fixed. Obviously, the user can write a script to iterate over a list of voltage values, set the voltage of a TEC object, then query the object for the output power density and record the result. This approach is a decent first step, but it has many problems:
  
  * What should the structure of the output data be?
  * How do we couple the script used to generate the data to the data itself for purposes of provenance?
  * Recording only two arrays of data is throwing away a lot of useful metadata and computer time -- how do we capture that metadata and avoid re-calculating all that data?
  * Is there an easy way of visualizing the data the script author intended to calculate?
  
The purpose of the tec package scripting system is to address all of those questions. The scripting system allows the user to write a script to generate data from the tec library so that the script itself and any TEC objects that are created are all put into a dict-like structure and saved to a file using the python pickle module. The scripting system also provides functionality so that the user can define a way to visualize the data that was generated. In this way no expensive data is lost during the execution of the script, the script itself is saved along with the data, and visualization of the data the script's author wanted is straightforward.


Testing
=======
Testing the tec package breaks down into two components: logical testing and numerical testing. The testing regime is liberally documented.

Logical testing
---------------
Tests of the functionality of a class, tests for graceful failures upon bad input, and essentially any functionality that is not a calculation are considered logical tests. These tests mainly follow the API and the docstrings of the classes and methods. The docstrings of the tests themselves contain any necessary details.

Numerical testing
-----------------
Numerical tests evaluate the accuracy of the output of methods that return a quantitative value and provide assurance that calculations are being performed properly. These methods are referred to as calculator methods. Fully evaluating all possible inputs to any particular calculation is impractical. The implementation of the numerical testing regime has several parts, but the rationale boils down to individually evaluating the uncertainty of every calculator method. Numerical accuracy is tested with the unit testing framework. Each calculator method requires the following items in order to be considered to be fully tested.

  * A unit listed in the method's docstring.
  * A value of uncertainty listed in the method's docstring as well as the corresponding tests' docstrings.
  * An analysis of the method's uncertainty documented in that method's test's docstring.
  * A standard set of data, typically a set of special cases (explained below).
  * A script that generates the standard data.
  * A unit test that tests the method against the standard data.
  * Additional unit tests that test any other special, edge, or corner cases.
  
Generally, each calculator method will have one main numerical test where all the above documentation will be located.
  
Distinguishment between classification of various cases is important in this discussion. "Special case" refers to a case that gives a mathematically unique result. For example, some combination of parameters may yield an output current density of precisely 10 A cm^{-2}. "Edge case" refers to the situation where one parameter is pushed to its limit. "Corner case" refers to the situation where more than one parameter is at an extreme but allowed value and where errors might occur.

Uncertainty analysis, uncertainty quantification, and units
...........................................................
Analysis of the uncertainty of a calculator method will be included in the docstring of the test of that method. Additional rationale behind a numerical test will also be included in the docstring of that test. Especially for the motive calculators, the numerical tests will follow the description of the algorithm in those methods' docstrings. The unit and value of relative uncertainty of the return value of a calculator method will be quoted in the summary line of the method docstring and test docstring.

Taylor (ISBN: 978-0-935702-42-2) goes into great detail regarding how uncertainty propagates through simple calculations. There is no reason to treat machine numbers and uncertainty propagation in the machine any differently than Taylor would treat a measured value with an uncertainty.

The majority of the calculator methods in the tec package are straightforward mathematical operations like multiplication, division, addition, subtraction, and things like exp(). These calculator methods can be thought of as very simple algorithms; they are just a one-line calculation. I can very easily evaluate the uncertainty propagation through these calculators and determine what it means to pass these tests. Subclasses of the TEC class will generally only overload methods related to calculating the motive, not methods that calculate the output current density, output voltage, etc. Uncertainty in the motive calculation algorithm will typically enter these other methods as a single value. The result is that the output of the non-motive calculators may be numerically inaccurate, but the calculator algorithm is still returning values that are acceptably precise. In other words, the simple calculator methods may be precisely calculating the wrong answer.

The point is that I can write numerical tests for all of the methods in the base TEC class. If the simple calculators pass the tests, I can rest assured that changing  the motive calculator won't affect the accuracy of these simple calculator methods. Therefore, child classes only require evaluation and testing of the method used to calculate the motive, not any simple calculator method.

In the calculator methods there are three sources of uncertainty. One, the machine isn't perfectly precise: I'm pretty sure that all the numbers are kept to double precision. In other words, the machine can only approximate irrational numbers like \pi and sqrt(2). Therefore, the machine propagates uncertainty through calculations and any number which is a result of a calculation has some uncertainty.

In the case of parameters I use as inputs (e.g. emitter temperature or collector voltage) I assume the number has machine precision regardless of the number of decimals I specify. Assuming there are 15 decimals worth of precision, if I specify the emitter barrier height as 

  1.4
  
I am effectively saying it is 

  1.40000000000000
  
This construction is a little silly, but it is what I am doing.

The second source of error are the values of the physical constants I use. I will use the most precise values I can find, but these values are always reported to a certain precision with a particular uncertainty. I believe this precision is less than the machine precision and therefore will be the predominant source of uncertainty in a value returned by a calculator method.

One final source of uncertainty, related to the uncertainty of physical constants, arises from the conversion of units. Converting cm^2 into m^2 doesn't change the relative uncertainty because there is an absolutely precise relationship between cm and m. In fact, Taylor mentions such a convention on p. 54. Converting other units like eV to J comes with an uncertainty because the conversion factor isn't absolutely precise -- in this case it is the value of the fundamental charge.

Unit tests for numerical accuracy
.................................
The general numerical testing procedure is as follows. The test starts with a list of known inputs and outputs, referred to as a "standard." Each item in the list has a collection of input values and a corresponding output value, typically contained in a dict. The range of input values spans the range of interesting values for the problem. The test iterates over the items in the standard list. For each item, the test uses the inputs to initialize the calculation and get the value of the result of the calculation. The test compares the returned value to the standard value. The test is passed when the method returns values that are equal to the standard values within the uncertainty of the calculation. This strategy is implemented as a specific unit test.

Edge case and corner case calculations are implemented as unit tests where necessary.

Standard data and scripts to generate it
........................................
The numerical tests require standard sets of data. These data will usually conform to the following guidelines unless noted:

  * Each collection of input values and output value is a special case.
  * The standard data spans the ranges of interesting values of the input parameters.
  * There aren't a large number of items in the set of standard data. This requirement ensures that a person can spot-check the data in a reasonable amount of time and effort.
  
Each standard set of data will have a script used to generate it. The naming scheme for the data is:
  
    Class.method_name_STANDARD.dat

and the naming scheme for the corresponding generator script is:
  
    Class.method_name_STANDARD.py  

Special cases are chosen for the data to make it easy for a human to spot check the results. The scripts are usually developed in the ipython notebook or by first executing all the calculations in ipython, saving the commands and outputs to a file with

>>> %logstart -o

and then cleaning up and commenting the result in a text editor.


NOTE: Generalize and add most of the docstring for Electrode.calc_saturation_current_STANDARD.py? The point here is to write all of the general conventions in this document and leave the docstrings as the place to put specifics or irregular cases.

"""
Generates the standard data for the Electrode calc_saturation_current method.

This script was modified from an ipython session to calculate some special case sets of parameters with outputs. By "special case" I mean the following: a set of parameters which yield a value of output current density that is a single digit (within precision of the calc_saturation_current method) times some power of 10. For example, 2e7. I chose to use the recorded output of an ipython session because I am only testing 8 sets of parameters and it is not that much code to visually parse and check the values by hand if one is so inclined.

The parameters and corresponding output value is collected together in a dict, and appended to a list. At the end of the script, the list is pickled and written to a file for use in the numerical testing strategy described in the README.

The input parameters were chosen to span the range of interesting parameters, given below.

  barrier_ht: [0.5, 5.0]
  temp:       [200, 2000]
  richardson: [0.01, 100]
"""

NOTE: I need some commentary on why its ok to calculate only a small set of data. I need to talk about how I assume the computer calculates things deterministically and consistantly.
