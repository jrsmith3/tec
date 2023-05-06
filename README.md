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


## Exploring via Jupyter notebook
This repo contains an example Jupyter notebook to facilitate exploring
the package. The notebook is located at
[`doc/examples.ipynb`](doc/examples.ipynb). This repo also includes a
`tox` environment to build the `tec` package, install its
dependencies, install Jupyter and its dependencies, and then run the
Jupyter server. For more information about `tox`, see below.

The `tox` command is as follows.

```bash
tox run -e nb
```


## License
MIT


## Development
This repository uses [`tox`](https://tox.wiki/en/latest) for most of
its automation, so install it before hacking on the source.

```bash
# Install dependencies for development.
pip install tox
```


To run the tests, just call `tox`. `tox` will install the necessary
dependencies (e.g. `pytest`) in a virtual environment, build the
package, install the package that was built (which is
[a good practice](https://blog.ionelmc.ro/2014/05/25/python-packaging))
into that virtual environment, then call `pytest` to run the tests.

```bash
# Run the tests in your local environment.
tox
```


This repo also features GitHub workflows for continuous integration
automations. Some of these automations leverage `tox` as well, and
there are corresponding `tox` environments defined in the `tox.ini`
file. These `tox` environments are not intended to be run on a
developer's machine -- see the `tox` config and the automation
definitions in the `.github` subdirectory for information on how they
work.

Version numbers are [`PEP-440`](https://peps.python.org/pep-0440/)
compliant. Versions are indicated by a tagged commit in the repo
(i.e. a "version tag"). Version tags are formatted as a "version
string"; version strings include a literal "v" prefix followed by a
string that can be parsed according to `PEP-440`. For example:
`v2.0.0` and not simply `2.0.0`. Such version strings will have three
components, MAJOR.MINOR.PATCH, which follow clauses 1-8 of the
[semver 2.0.0 specification](https://semver.org). Any documentation
change by itself will result in an increment of the PATCH component
of the version string.

All commits to the `main` branch will be tagged releases. There is no
`dev` branch in this repo. This repo may include post-release
versions. Such post-release versions correspond to changes to the
development infrastructure and not functional changes to the
codebase.

This repo includes a GitHub workflow to automatically build the
package, test the package, and create a GitHub release. Version tags
are manually created by me (Joshua Ryan Smith) in my local clone of
the repo. Therefore, releasing is semi-automated but is initiated by
a manual tagging process. I.e. when I want to create a new release, I
create a version tag in the repo and push that tag -- the GitHub
workflows take care of the rest. Such version tags should be
annotated. The tag message should include the list of issues that are
included in the release.
