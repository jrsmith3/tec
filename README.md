# tec - Utils for simulating thermoelectron energy conversion devices
A
[thermoelectron energy conversion device](https://en.wikipedia.org/wiki/Thermionic_converter)
(TEC) is a vacuum or vapor device that converts heat directly to
electrical work and is based on the phenomenon of
[thermoelectron emission](https://en.wikipedia.org/wiki/Thermionic_emission)
(often called _thermionic_ emission). This package includes utilities
for simulating the performance of TECs.


## Quickstart
The quickest way to begin exploring the package is to launch a Jupyter
server via the included `tox` environment, then look at the examples
in the example notebook located at
[`doc/examples.ipynb`](doc/examples.ipynb).

```bash
tox run -e nb
```

If you are interested in a command-line approach, it is given below.

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


## Development
This repository uses [`tox`](https://tox.wiki/en/latest) for most of
its automation, so install it before hacking on the source.

```bash
# Install dependencies for development.
pip install tox
```


I have included several development functionalities for `tox`; see the
`tox.ini` for full details. Some of the common development
functionalities are listed below.

```bash
# Buld package, install pacakge, and run tests locally.
# (a good practice:
# https://blog.ionelmc.ro/2014/05/25/python-packaging)
tox run -e test


# Build package and copy build artifact to `tec/dist`.
tox run -e preserve_build


# Build pacakge and copy build artifact to `/tmp/build` by setting the
# value of the `JRS_DIST_DIR` environment variable.
JRS_DIST_DIR=/tmp/build tox run -e preserve_build


# Build package, run tests, and preserve the package artifact in the 
# `tec/dist` directory.
tox run -e test,preserve_build
```


### Versioning and releases
Certain commits in the repo correspond to a particular version of the
software. Such commits are indicated by a "version tag": a signed,
annotated git tag with a specific format called a "version string." A
version string begins with a literal "v", and is formatted according
to [`PEP-440`](https://peps.python.org/pep-0440/). Version strings
will have three components, MAJOR.MINOR.PATCH, which follow clauses
1-8 of the [semver 2.0.0 specification](https://semver.org). An
example of a version string is `v2.0.0`; `2.0.0` could correspond to
a particular version of the software, but would not be a version
string since it is missing the "v" prefix.

All commits on the `main` branch of the repo will be tagged with a
version tag. Version strings formatted as
["final releases"](https://peps.python.org/pep-0440/#final-releases)
(e.g. `v2.0.0`) and
["post-releases"](https://peps.python.org/pep-0440/#post-releases)
(e.g. `v2.0.0.post1`) will only ever appear on the `main` branch,
never another branch. Version strings formatted as
["pre-releases"](https://peps.python.org/pep-0440/#pre-releases) may
appear on any branch, including `main`; typically release candidate
pre-release tags (i.e. version strings with the `rc` suffix) should
coincide with a final release tag on `main`.

Any documentation change by itself will result in an increment of the
PATCH component of the version string. Post-release version tags
correspond to changes to the development infrastructure and not
functional changes to the codebase.

Version tags are created manually by me (Joshua Ryan Smith) in my
local clone of the repo. This repo includes automation to create a
GitHub release when a version tag is pushed. Pre-release version tags
will result in pre-release releases, while final release version tags
will result in actual releases. Post-release version tags will not
result in a GitHub release being created since the functionality of
the codebase has not been changed. The tag message should include a
list of issues that are included in the release; copying from the
`CHANGELOG` is sufficient.


## Automation via GitHub actions
This repo contains several automations located in the
`.github/workflows` subdirectory. These automations leverage the
`tox` functionalities described above. See the source of these
workflows for more details about their behavior, input parameters,
and return values.
