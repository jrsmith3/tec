# tec - Utils for simulating thermoelectron energy conversion devices
A
[thermoelectron energy conversion device](https://en.wikipedia.org/wiki/Thermionic_converter)
(TEC) is a vacuum or vapor device that converts heat directly to
electrical work and is based on the phenomenon of
[thermoelectron emission](https://en.wikipedia.org/wiki/Thermionic_emission)
(often called _thermionic_ emission). This package includes utilities
for simulating the performance of TECs.


## Quickstart
I have not yet published recent packages to pypi, so the only wayt to
run the code at this time is to clone the repo and use the source. I
am using [hatch](https://hatch.pypa.io/latest/) to manage the
packaging, so it is fairly easy to create a virtual environment to
get started.

```bash
# Clone the repo
git clone git@github.com:jrsmith3/tec.git

# Install hatch
pip install hatch

# Create a virtual environment with the code from the current commit
hatch shell
```


The code is object-oriented, and instances of `TEC` objects are the
interface with which the user will mainly interact. `TEC` objects
provide functionality to compute interesting quantities of a device
such as output current density, output power density, efficiency,
etc. `TEC` objects are comprised a model object, which in turn is
comprised of electrode objects. A model class contains the code
necessary to implement a particular model: for example, the ideal
model (ignores the negative space charge effect) or Langmuir model
(accounts for the negative space charge effect, ignores back
emission) of a vacuum TEC.

Despite the nested structure of the `TEC`, model, and electrode
objects described above, attributes of both the model and electrodes
are easily accessible from the `TEC` instance -- examples are given
below.

Even though users will mainly interact with `TEC` objects, model
classes feature a class method `from_args` which conveniently takes
a (flattend) set of parameters which fully describe the device and
returns a `TEC` instance. This class method is demonstrated in the
following example.


```python
import tec

device = tec.models.Ideal.from_args(
            emitter_temperature = 2000,
            emitter_barrier = 2,
            collector_temperature = 300,
            collector_barrier = 0.8,
            collector_voltage = 5,
            collector_position = 10,
    )

device.output_current_density()  # Returns <Quantity 1.16381647e-06 A / cm2>
device.output_power_density()  # Returns <Quantity 5.81908236e-06 W / cm2>
device.carnot_efficiency()  # Returns <Quantity 0.85>
device.efficiency()  # Returns <Quantity 6.41715705e-08>


# Inspect the device's electrode properties
device.emitter.temperature  # <Quantity 2000. K>
device.collector.barrier  # <Quantity 0.8 eV>


# Many properties have default values
device.emitter.richardson  # <Quantity 120. A / (cm2 K2)>
```


Note that `TEC`, model, and electrode instances are static -- once an
object has been instantiated, its properties cannot be changed. If
you want an instance with a different value for a property, a new
instance must be created.


## License
MIT
