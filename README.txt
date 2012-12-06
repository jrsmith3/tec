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
At the heart of the tec package is the TEC class. This class implements the functionality of a thermionic energy conversion device. To simulate the performance of a TEC, the user instantiates a TEC object and calls methods to acquire data about its present state (e.g. output power density, efficiency, etc.).

There are many different models of electron transport through a TEC. A major objective of the TEC class is to provide a generic interface for the user without requiring the user to understand the arcane specificities of the particular model. The TEC class is written so that it can be subclassed in order to implement an arbitrary model.

The question at the heart of all models of electron transport across a TEC is: how is the electron motive calculated? Therefore, the TEC class and any subclass essentially addresses that question. The TEC class is instantiated with data describing its state (e.g. emitter temperature, collector emissivity, etc. -- see Sec. <REF>). A call to a method of the TEC class results in the calculation of the electron motive and any associated model-dependent metadata. Acquiring this data and metadata is generally the most computationally intensive calculation that m must be performed and so it is calculated only once and stored in the TEC object for subsequent calculations. If the data of the TEC object is modified so as to change the motive, the motive data and metadata of the TEC object is deleted and new motive data and metadata is calculated. The TEC class provides methods to retrieve the data and metadata associated with the calculation of the motive. The nature of this data and metadata may vary depending on the specifics of the model. the TEC class and any subclass has a description of the algorithm used to calculate the motive as well as a description of the data and metadata generated during the calculation of the motive.

The TEC class treats its data similar to a python dictionary. TEC objects have two data fields: Emitter and Collector. The data of each field is an Electrode object. The data for each electrode of the TEC is enough to fully specify the state of the TEC object. As mentioned previously, the TEC class provides methods to return values of interest to the user such as output power density, Carnot efficiency, or back current density (see the class documentation for specifics).

A few models are provided with the tec package, but here I will only describe the parent class. See the class documentation and source code of the other classes for more details. The TEC parent class implements the most basic model: it ignores the negative space charge effect and calculates a linear motive between the emitter vacuum level and collector vacuum level.


Scripting System
================
The classes and API of the tec package's library were designed to create a generic interface separate from the implementation details of any particular model. While this design is useful, it doesn't completely address all of the requirements a user has; for example, many times a user is interested in seeing the output power density vs. voltage of a device who's other parameters remain fixed. Obviously, the user can write a script to iterate over a list of voltage values, set the voltage of a TEC object, then query the object for the output power density and record the result. This approach is a decent first step, but it has many problems:
  
  * What should the structure of the output data be?
  * How do we couple the script used to generate the data to the data itself for purposes of provenance?
  * Recording only two arrays of data is throwing away a lot of useful metadata and computer time -- how do we capture that metadata and avoid re-calculating all that data?
  * Is there an easy way of visualizing the data the script author intended to calculate?
  
The purpose of the tec package scripting system is to address all of those questions. The scripting system allows the user to write a script to generate data from the tec library so that the script itself and any TEC objects that are created are all put into a dict-like structure and saved to a file using the python pickle module. The scripting system also provides functionality so that the user can define a way to visualize the data that was generated. In this way no expensive data is lost during the execution of the script, the script itself is saved along with the data, and visualization of the data the script's author wanted is straightforward.


Numerical Testing
=================
I am at the point where I have to write tests for numerical routines and I want to ensure that the numerical values my various methods return are sufficiently accurate. I pretty much am facing two problems:
  1. Is the number produced by my standard data generator equal to the number produced by the method under test?
  2. I am testing a subset of the total number of values that can be calculated. How confident am I that a value outside of that subset is accurate?
  
Before I get too deep into the details, let me take a step back and think about my general numerical testing strategy.

The sequence I intend to use to test numerical accuracy of a method is as follows. I will have a set of standard data for that method. This standard data will consist of inputs and an output. I will iterate over the list of standard data. For each item, I will use the inputs to initialize the object, then I will call the method in question and compare its output to the standard output. these values will need to match to within an acceptable discrepancy. If there are any cases in which the values do not match, the numerical test will be considered to have failed.

A permutation of this test will be as follows. For some cases, the output of a method can provably be less than, greater than, less than or equal to, etc. one of the standard sets of data.

The advantage of this approach is that it fits nicely within the typical python unit testing framework. Once the standard sets of data have been generated, they can be reused every time the unit tests are run.

There are a number of issues that must be addressed for this numerical testing strategy to work. In no particular order:
  
  1. I have to believe that all of the values in the standard set of data are accurate.
  2. I have to understand the precision of the values in the standard set of data. It may be that I can only believe the first number after the decimal. If that is the case, a difference of ~1e-2 between the standard value and the value returned by a method is acceptable.
  3. I have to be convinced that the method under test is accurate despite the fact that I'm only testing a small number of possible values.
  
Here are some ways that I will address the above three points, again, in no particular order.

2. Precision
------------
For any numerical calculation, there is a way to determine the precision of the result given the precision of the input. For example, given a set of parameters (T, \phi, A), I can say that the output current density of Richardson-Dushmann is precise to a specific number of decimal places. Furthermore, I can determine the precision of the value of the output of any particular method in a similar fashion. At that point, I am evaluating the equality of the two values within their own precision.

This reasoning leads me to another issue: it is important that the standard data or the values returned by a method have a specific precision? I think the precision of the values is probably limited by the precision of the physical constants I am using.

1. Accuracy of standard data
----------------------------
I am very confident that 2 + 3 = 5. I am also confident that 2 * 2.5 = 5. I'm confident because these are very simple calculations I can spot check. Given some time, I'm fairly confident I can compute:
  
  1.4/(5.67e-5 * 673)
  
but computing such products/quotients by hand doesn't scale. Since the above product/quotient is a tedious hand calculation, I would not be confident that I could accurately do more than two or three at a time. Therefore, calculating thousands or even hundreds of values of standard data by hand is a non-starter. Even calculating tens of such values is likely too time consuming.

So what is the strategy?

I had two strategy ideas for this problem. One is to use special case values. The other is to use an ipython notebook. Both actually depend on my solution to issue 3.

Special case values
...................
Consider the Richardson-Dushmann equation:
  
  J = A * T**2 * exp(-\phi / (k * T))
  
There exist special sets of parameters A, T, and \phi such that J is a straightforward value of 1, 2, 10, 100, etc. I bet that, over the ranges of interest of all these parameters, enough special sets of values exist to test the entire space. At this point, I just need to convince myself that I have enough values over the entire parameter space that passing the test I described above ensures the accuracy of a method.

ipython notebook
................
The idea here was to generate some standard set of data using the ipython notebook. I would start with lists of values for each input value. These lists would span the parameter space of interest. I would write the ipython notebook so the calculation would happen piecewise. From my notes on 2012.11.21 p2:
  
  J = A * T**2 * exp(-\phi / (k * T))
  
  1. k * T        = ans1
  2. -\phi / ans1 = ans2
  3. exp(ans2)    = ans3
  4. T ** 2       = ans4
  6. A * ans4     = ans5
  7. ans3 * ans5  = output_value
  
The idea here is that it would be easy to spot check all the values ans1...ans5 and output_value. I could use this method on a small subset of data to check the values of the standard data set generator. Using a small subset of values to check a larger set of values is essentially the same problem as 3 above. So the question is: why not just skip the middle-man standard dataset and go straight to the method under test?

3. Accuracy despite testing a small number of values
----------------------------------------------------
I suspect this problem is akin to interpolation. The method under test is essentially a black box. Because of the nature of computers, the inputs aren't really continuous, but they span some large number of states due to double precision floating point numbers. I am taking a very small subset of values and testing them and expecting all other values to be accurate as a result of passing the test.

I just looked over the first three chapters of Taylor (ISBN: 978-0-935702-42-2). In it he talks about uncertainties in measurements and how those uncertainties propagate. It looks like the rest of the book is concerned with statistical distributions and quantitative ways of determining what a real uncertainty is.

How does this information relate to the question at hand? The question at hand is: how do I test the numerical result of the methods of my various classes? I thin the main takeaway of what I just read is: there is a deterministic procedure for determining the uncertainty in the value of a calculated number, given the uncertainties in the inputs of the calculation. In the event that two uncertain numbers need to be compared to be equal, they are equal if they match within their own uncertainties.

In  my calculations, there are two sources of uncertainty. One, the machine isn't perfectly precise: I'm pretty sure that all the numbers are kept to double precision. In other words, the machine can only approximate irrational numbers like \pi and sqrt(2). Therefore, the machine propagates uncertainty through calculations and any number which is a result of a calculation has some uncertainty.

In the case of parameters I use as inputs (e.g. emitter temperature or collector voltage) I assume the number has machine precision regardless of the number of decimals I specify. Assuming there are 15 decimals worth of precision, if I specify the emitter barrier height as 

  1.4
  
I am effectively saying it is 

  1.40000000000000
  
This construction is a little silly, but it is what I am doing.

The other source of error are the values of the physical constants I use. I will use the most precise values I can find, but these values are always reported to a certain precision with a particular uncertainty. I believe this precision is less than the machine precision and therefore will be the predominant source of uncertainty in a value returned by a calculator method.

One final source of uncertainty might arise from the conversion of units. Converting cm^2 into m^2 doesn't change the uncertainty (I don't think) because there is an absolutely precise relationship between cm and m. In fact, Taylor mentions such a convention on p. 54. The uncertainty just scales it looks like. Converting other units like eV to J probably does come with an uncertainty because the conversion factor isn't absolutely precise and I think is typically derived from fundamental physical constants.

Here is the big takeaway: I believe that comparing a method's calculated value to a standard value is a legitimate strategy to test for numerical accuracy with a few caveats. First, there is uncertainty in both the standard value and the method's calculated value; comparing these two numbers requires consideration of those uncertainties. Second, I want to be conservative in my interpretation of what it means to pass the test against a list of standard values. The test I propose I defined above: I have a list of standard input s and outputs; each item in the list has a collection of input values and a corresponding output value. The range of input values spans the range of interesting values for the problem. I iterate over the items in the standard list. For each item, I use the inputs to initialize the calculation and get the value of the result so the calculation. I compare the returned value to the standard value, considering the uncertainty of both values. the test is passed when the method returns values that are equivalent to the standard values.

Like I said, I want to be conservative in my interpretation of the results of this test.

I see no reason to treat machine numbers and uncertainty propagation in the machine any differently than Taylor would treat a measured value with an uncertainty.

The computer treats numbers as a finite discrete set (the set is big, but finite). The list of standard values is another (much much smaller) discrete finite set. The test I describe above tests a method on a small subset of the possible values. It isn't fair to conclude that because the test is passed on the small subset, the method will return numerically accurate values for all the untested cases.

I think the bottom line here is that every method should be considered on a case-by-case basis. I have an approach involving interpolation for, e.g., the Electrode.calc_output_current_density() method, but I'll table the description for now. I think that an honest and thorough analysis of the numerical accuracy  of a class's methods involves the study of algorithms.

Consider the Electrode.calc_output_current_density() (or whatever I named it) method. This method is an implementation of the Richardson-Dushmann equation. I suppose I have an algorithm for this method, but the algorithm is pretty much a series of arithmetic operations (and an exp, but whatever) which are perfectly deterministic to a perfectly deterministic degree of precision. For these one-step calculation algorithms, I think it is safe to say that if the method in question passes the test against the standard described above, it is likely correct. The value of these tests are they catch boneheaded errors that may zing me later.

So numerical testing boils down to the analysis of algorithms. There are some very simple algorithms which are just some combination of mathematical operations. I will accept the claim that such a method "works" for all input values if it passes the test I described previously.

I want to mention a few thoughts I have on numerically testing more complex algorithms, but first I want to sketch out my interpolation testing scheme even though I am not going to implement it.

Interpolation testing
.....................
Consider again the Electrode.calc_output_current_density(). I calculate a small subset of values across a range of input values. I could turn that set of inputs into some kind of multidimensional mesh and create a multidimensional interpolation. This interpolation approximates the output value at all points in space with a provable uncertainty (say O(3) or however you write it). I could pick a random set of points in input parameter space, use those points as inputs to the method under test, and compare the returned outputs to the corresponding outputs returned by the interpolation. Since I know the uncertainty of both outputs, I can do a comparison considering the uncertainty like before. Since I've introduced a stochastic element in the test, I can make a claim on the confidence I have in the numerical accuracy.

I'm not going to do that, but it felt good to write it down.

More complex algorithms
.......................
I think the trick to analyzing the numerical accuracy of a more complex algorithm is as follows. First, that algorithm must converge. Second, uncertainty will propagate through the algorithm in a way that can be evaluated similarly to the very simple one-line calculations. The trick is to analyze and document carefully the algorithms I use.

This is worth mentioning if I haven't already: numerical testing boils down to evaluating algorithms. Most of my algorithms are essentially single-step direct calculations and so therefore I only need to test them once. This approach is good software development because it means I can isolate different parts of the code and test it independently. Practically speaking, a consequence is that I only have to test algorithms like calculating the output power density or efficiency of the TEC class only once. The thing that changes among models is the method used to calculate the motive. That method manifests itself in, e.g., the output power density calculation as a single value that is multiplied/divided/added/subtracted by other values. Therefore, as long as that single value is accurate, the rest of the output power density calculator algorithm remains accurate. So the point is that for new models, I only have to evaluate the algorithm I use to calculate the motive.