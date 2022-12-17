# coding: utf-8
"""
Base Library (:mod:`tec`)
=========================
A thermoelectron energy conversion device (TEC) converts heat directly
to electrical work via the phenomenon of thermoelectron emission.
This package provides implementations of models of TECs and some
additional functionality for computing quantities of interest such as
output current density, output power density, efficiency, and
others.


Organization
------------
The main interface is the `TEC` object, located directly beneath the
package root namespace: `tec.TEC`. A `TEC` instance contains all of
the relevant parameters such as emitter temperature, emitter barrier,
collector temperature, etc. as well as methods to compute interesting
quantities like output power density. A `TEC` instance does not
implement any particular model; model implementation details are
specified in a `Model` object. Examples of models include the model
which ignores the effect of space charge but accounts for back
emission, the model which accounts for space charge but ignores back
emission (cf. Langmuir (CITE)), etc. To provide functionality, a
`TEC` instance wraps an instance of a `Model` object, and a `Model`
object provides the minimum functionality necessary for the `TEC` to
compute its outputs. Specifically, a `Model` object provides
functionality to compute information about the motive. Model
implementations can be found in the `tec.models` submodule.

This package also provides an `Electrode` class which is an
implementation of a TEC's electrode. The `Electrode` class contains
the data necessary to specify the electrode's properties
(temperature, barrier height, Richardson's constant, etc.) as well as
characteristic functionality such as thermoelectron current density.
Electrode implementations can be found in the `tec.electrodes`
submodule.

Instances of `Electrode` objects are used to instantiate `Model`
objects (along with any additional arguments specific to the
particular model), and a `Model` instance is used to instantiate a
`TEC`. Each `Model` provides a class method for conveniently
constructing a `TEC` from a flattened list of parameters.


.. currentmodule:: tec
"""

from . import electrode

try:
    from ._version import __version__
except ModuleNotFoundError:
    __version__ = ""
