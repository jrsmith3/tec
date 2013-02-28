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
  
Distinguishment between classification of various cases is important in this discussion. "Special case" refers to a case that gives a mathematically unique result, specifically an integer power of 10 within the precision of the calculation. For example, some combination of parameters may yield an output current density of precisely 10 A cm^{-2}. "Edge case" refers to the situation where one parameter is pushed to its limit. "Corner case" refers to the situation where more than one parameter is at an extreme but allowed value and where errors might occur.

Uncertainty analysis, uncertainty quantification, and units
...........................................................
Analysis of the uncertainty of a calculator method will be included in the docstring of the test of that method. Additional rationale behind a numerical test will also be included in the docstring of that test. Especially for the motive calculators, the numerical tests will follow the description of the algorithm in those methods' docstrings. The unit and value of relative uncertainty of the return value of a calculator method will be quoted in the summary line of the method docstring and test docstring.

Taylor (ISBN: 978-0-935702-42-2) goes into great detail regarding how uncertainty propagates through simple calculations. There is no reason to treat machine numbers and uncertainty propagation in the machine any differently than Taylor would treat a measured value with an uncertainty.

The majority of the calculator methods in the tec package are straightforward mathematical operations like multiplication, division, addition, subtraction, and things like exp(). These calculator methods can be thought of as very simple algorithms; they are just a one-line calculation. I can very easily evaluate the uncertainty propagation through these calculators and determine what it means to pass these tests. Subclasses of the TEC class will generally only overload methods related to calculating the motive, not methods that calculate the output current density, output voltage, etc. Uncertainty in the motive calculation algorithm will typically enter these other methods as a single value. The result is that the output of the non-motive calculators may be numerically inaccurate, but the calculator algorithm is still returning values that are acceptably precise. In other words, the simple calculator methods may be precisely calculating the wrong answer.

The point is that I can write numerical tests for all of the methods in the base TEC class. If the simple calculators pass the tests, I can rest assured that changing  the motive calculator won't affect the precision of these simple calculator methods. Therefore, child classes only require evaluation and testing of the method used to calculate the motive, not any simple calculator method.

In the calculator methods there are three sources of uncertainty. One, the machine isn't perfectly precise: I'm pretty sure that all the numbers are kept to double precision. In other words, the machine can only approximate irrational numbers like \pi and sqrt(2). Therefore, the machine propagates uncertainty through calculations and any number which is a result of a calculation has some uncertainty.

In the case of parameters I use as inputs (e.g. emitter temperature or collector voltage) I assume the number has machine precision regardless of the number of decimals I specify. Assuming there are 15 decimals worth of precision, if I specify the emitter barrier height as 

  1.4
  
I am effectively saying it is 

  1.40000000000000
  
This construction is a little silly, but it is what I am doing.

The second source of error are the values of the physical constants I use. I will use the most precise values I can find, but these values are always reported to a certain precision with a particular uncertainty. I believe this precision is less than the machine precision and therefore will be the predominant source of uncertainty in a value returned by a calculator method.

One final source of uncertainty, related to the uncertainty of physical constants, arises from the conversion of units. Converting cm^2 into m^2 doesn't change the relative uncertainty because there is an absolutely precise relationship between cm and m. In fact, Taylor mentions such a convention on p. 54. Converting other units like eV to J comes with an uncertainty because the conversion factor isn't absolutely precise -- in this case it is the value of the fundamental charge. The uncertainty of unit conversion of object data is noted in the docstring of the class.

Unit tests for numerical accuracy
.................................
The general numerical testing procedure is as follows. The test starts with a list of collections of known inputs and outputs, referred to as a "standard." Each item in the list has a collection of input values and a corresponding output value, typically contained in a dict. The range of input values spans the range of interesting values for the problem. The test iterates over the items in the standard list. For each item, the test uses the inputs to initialize the calculation and get the value of the result of the calculation. The test compares the returned value to the standard value. The test is passed when the method returns values that are equal to the standard values within the uncertainty of the calculation. This strategy is implemented as a specific unit test.

Edge case and corner case calculations are implemented as unit tests where necessary.

Standard data and scripts to generate it
........................................
The numerical tests require standard sets of data. These data will usually conform to the following guidelines unless noted in the appropriate unit test docstring:

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

The usual structure of a standard generating script is as follows: the special case parameters and corresponding output value are collected together in a dict, and appended to a list. At the end of the script, the list is pickled and written to a file for use in the numerical testing.

This entire testing strategy is based on the assumption that the computer can accurately and repeatably do simple calculations. I assume that as far as the computer is concerned, the product

  2 * 5
  
is just as easy to calculate as the product

  2.333690544228055 * 5.44073192976832565

and the result is just as accurate. Most of the calculator methods are straightforward arthatical operations, and the real important task is to analyze the uncertainty propagation.

The other assumption I'm making is that for every calculator method there is a tremendous number of combinations of input paramters. The problem isn't that it would take an unacceptably long time with unacceptably lare computing resources to exhaustively calculate all of those combinations. The problem is that there's no reasonable way to check the standard set of data.

Since checking a comprehensive standard set of data is unreasonable, the next approach would be to have a much smaller set of standard data which is a subset of hte comprehensive set of standard data. The question now becomes: how small does the subset need to be? If the subset gets too big, the problem of reasonably checking all the values reemerges.

Since we've already assumed that hte computer accurately and repeatably calculates simple arithmatic operations, the subset of standard data can be quite small. Since the ease with which a computer calculates an operation a human finds easy is the same as a similar operation a human finds hard, it is best to choose special case parameters so that humans can quickly spot-check all of the standard data.

The bottom line is that the foundation of this testing strategy is to check the uncertainty propagation of each algorithm to get a picture of the uncertainty of compound algorithms. The strategy of checking algorithms is much better than slavishly checking sets of standard data.



There are a number of issues that must be addressed for this numerical testing strategy to work. In no particular order:
  
1. I have to believe that all the values in the standard set of data are accurate.
2. I have to understand the precision of the values in the standard set of data. It may be that I can only believe the first number after the decimal. If that's the case, a difference of ~1e-2 between the standard value and the value returned by a method is acceptable.
3. I have to be convinced that the method under test is accurate despite the fact that I'm only testing a small number of possible values.
  
2. Precision: For any numerical calculation, there is a way to determine the precision of the result given the precision of hte input. For example, given a set of parameters (T, \phi, A), I can say that the output current density of the Richardson Dushamann equation is precise to a particular number of decimal places. Furthermore, I can determine the precision of the value of the output of any particular method in a similar fashion. At that point, I am evaluating the equality of the two values within their own precision.

1. Accuracy of standard data: I am very confident that 2 + 3 = 5. I'm confident because it is a very simple calculation I can spot check. Given some time, I am fairly confident I can compute:
  
  1.4/(5.67e-5 * 673)
  
but computing such products and quotients by hand doesn't scale. Since the above product/quotient is a tedious hand calculation, I would not be confident that I could accurately do more than two or three at a time. Therefore, calculating thousands or even hundreds of standard data by hand is a non-starter. Even calculating tens of such values is likely too time consuming.

3. Accuracy despite testing a small number of values: I suspect this problem is akin to interpolation. The method under test is essentially a black box. Because of the nature of computers, the inputs aren't really continuous, but they span some large number of states due to double precision floating point numbers. I am taking a very small subset of values and testing them and expecting all other values to be accurate as a result of passing the test.