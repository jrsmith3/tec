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
Numerical tests evaluate the output of methods that return a quantitative value. Fully evaluating all possible inputs to any particular calculation is impractical. The strategy for numerical testing involves evaluating every algorithm that produces a numerical result and determining the algorithm's numerical precision.

The general numerical testing procedure is as follows. The test starts with a list of standard inputs and outputs; each item in the list has a collection of input values and a corresponding output value. The range of input values spans the range of interesting values for the problem. The test iterates over the items in the standard list. For each item, the test uses the inputs to initialize the calculation and get the value of the result of the calculation. The test compares the returned value to the standard value, considering the uncertainty of both values. The test is passed when the method returns values that are equal to the standard values within the uncertainty of the calculation.

This strategy is implemented as a specific unit test. These tests will be executed from time to time and the purpose is to catch boneheaded errors that may creep in when code is modified.

Taylor (ISBN: 978-0-935702-42-2) goes into great detail regarding how uncertainty propagates through simple calculations. There is no reason to treat machine numbers and uncertainty propagation in the machine any differently than Taylor would treat a measured value with an uncertainty.

The majority of the calculator methods in the tec package are straightforward mathematical operations like multiplication, division, addition, subtraction, and things like exp(). These calculator methods can be throught of as very simple algorithms; they are just a one-line calculation. I can very easily evaluate the uncertainty propagation through these calculators and determine what it means to pass these tests. Subclasses of the TEC class will generally only overload methods related to calculating hte motive, not methods that calculate the output current density, output voltage, etc. Uncertainty in the motive calculation algorithm will typically enter these other methods as a single value. The result is that the output of the non-motive calculators may be numerically inaccurate, but the calculator algorithm is still self-consistantly returning values that are accurate. In other words, the simple calculator methods may be accurately calculating the wrong answer.

The point is that I can write numerical tests for all of the methods in the base TEC class. If the simple calculators pass the tests, I can rest assured that changing  hte motive claculator won't affect the accuracy of these simple calculator methods. Therefore, child classes only require evaluation and testing of the method used to calculate the motive, not any simple calculator method.

In  my calculations, there are two sources of uncertainty. One, the machine isn't perfectly precise: I'm pretty sure that all the numbers are kept to double precision. In other words, the machine can only approximate irrational numbers like \pi and sqrt(2). Therefore, the machine propagates uncertainty through calculations and any number which is a result of a calculation has some uncertainty.

In the case of parameters I use as inputs (e.g. emitter temperature or collector voltage) I assume the number has machine precision regardless of the number of decimals I specify. Assuming there are 15 decimals worth of precision, if I specify the emitter barrier height as 

  1.4
  
I am effectively saying it is 

  1.40000000000000
  
This construction is a little silly, but it is what I am doing.

The other source of error are the values of the physical constants I use. I will use the most precise values I can find, but these values are always reported to a certain precision with a particular uncertainty. I believe this precision is less than the machine precision and therefore will be the predominant source of uncertainty in a value returned by a calculator method.

One final source of uncertainty might arise from the conversion of units. Converting cm^2 into m^2 doesn't change the uncertainty (I don't think) because there is an absolutely precise relationship between cm and m. In fact, Taylor mentions such a convention on p. 54. The uncertainty just scales it looks like. Converting other units like eV to J probably does come with an uncertainty because the conversion factor isn't absolutely precise and I think is typically derived from fundamental physical constants.

I will include my analysis of the uncertainty of a calculator method in that method's docstring. I will include documentation of the rationale behind a numerical test in the docstring of that test. Especially for the motive calculators, the numerical tests will follow the description of the algorithm in those methods' docstrings.
