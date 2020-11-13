# crnsimulator 
Simulate Chemical Recation Networks (CRNs) using Ordinary Differential Equations (ODEs).

[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/bad-ants-fleet/crnsimulator)](https://github.com/bad-ants-fleet/crnsimulator/tags)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/bad-ants-fleet/crnsimulator?include_prereleases)](https://github.com/bad-ants-fleet/crnsimulator/releases)
[![PyPI version](https://badge.fury.io/py/crnsimulator.svg)](https://badge.fury.io/py/crnsimulator)
[![PyPI - License](https://img.shields.io/pypi/l/crnsimulator)](https://opensource.org/licenses/MIT)
[![Travis (.org)](https://img.shields.io/travis/bad-ants-fleet/crnsimulator)](https://travis-ci.com/github/bad-ants-fleet/crnsimulator)
[![Codecov](https://img.shields.io/codecov/c/github/bad-ants-fleet/crnsimulator)](https://codecov.io/gh/bad-ants-fleet/crnsimulator)

## Examples
### Using the `crnsimulator` executable:

Create a test file with your CRN:

File: [oscillator.crn]
```
# Rock-Paper-Scissors Oscillator

A + B -> B + B [k = 0.2]
B + C -> C + C [k = 0.4]
C + A -> A + A [k = 0.7]
```

And pipe it into the crnsimulator:
```sh
~$ crnsimulator -o ozzy < oscillator.crn
```
This writes the ODE system to an executable python script: `ozzy.py`

Check the command line parameters of ozzy.py. You have to set initial species
concentrations, and choose an output-format, e.g.:
```sh
~$ python ./ozzy.py --p0 A=0.1 B=1e-2 C=1e-3 --t8 10000 --pyplot ozzy.pdf
```
This example plots a simulation on a linear-time scale (0 - 10000) to the file `ozzy.pdf` .

### Tips and Tricks:

You can pass the command line options for ozzy.py directly to `crnsimulator`.
This will automatically simulate your ODE system. Use --force to overwrite an
existing `ozzy.py` script.
```sh
~$ crnsimulator --p0 A=0.1 B=1e-2 C=1e-3 --t8 10000 -o ozzy --pyplot ozzy.pdf < oscillator.crn
```

You can specify the CRN in a single line:

```sh
~$ echo "A+B->2B [k=0.2]; B+C->2C [k=0.4]; C+A->2A" | crnsimulator --p0 A=0.1 B=1e-2 C=1e-3 --t8 10000 -o ozzy --pyplot ozzy.pdf
```

You can specify default initial concentrations of species:

```sh
~$ echo "A @i 0.1; B @i 1e-2; A+B->2B [k=0.2]; B+C->2C [k=0.4]; C+A->2A" | crnsimulator --p0 C=1e-3 --t8 10000 -o ozzy --pyplot ozzy.pdf
```

If you can set which species appear in the legend using --pyplot-lables. If you 
are writing a new executable (you may need --force), then you can also control the order:

```sh
~$ echo "A @i 0.1; B @i 1e-2; A+B->2B [k=0.2]; B+C->2C [k=0.4]; C+A->2A" | crnsimulator --p0 C=1e-3 --t8 10000 -o ozzy --pyplot ozzy.pdf --force --pyplot-labels C B
```


### Using the `crnsimulator` library:

The easiest way to get started is by looking at the crnsimulator script itself.
However, here is a small example using the above oscillating CRN.

```py
>>> from crnsimulator import ReactionGraph
>>> crn  = [[['A', 'B'],['B','B'],0.2],
            [['B', 'C'],['C','C'],0.8],
            [['C', 'A'],['A','A'],0.9]]
>>> RG = ReactionGraph(crn)
>>> svars = ['B', 'C', 'A'] # let's enforce the order of species, because we can!
>>> filename, odename = RG.write_ODE_lib(filename='ozzy.py', sorted_vars = svars)
>>> print('Wrote ODE system file:', filename)
Wrote ODE system file: ozzy.py
```

Then go ahead and execute `ozzy.py`:
```sh
~$ python ./ozzy.py --p0 1=1e-6 2=2e-6 3=5e-6 --t8 1e8 --pyplot ozzy.pdf --atol 1e-10 --rtol 1e-10
```

... or load its functions by treating it as a python library:

```py
# Import
>>> import numpy as np
>>> from scipy.integrate import odeint
>>> from crnsimulator import get_integrator
>>> odesys = get_integrator(filename, function = odename)
>>> odeplt = get_integrator(filename, function = 'ode_plotter')
# Simulate
>>> p0 = [1e-6, 2e-6, 5e-6] # order of svars
>>> time = np.linspace(0, 1e8, num = 10_000)
>>> ny = odeint(odesys, p0, time, (None,), atol = 1e-10, rtol = 1e-10).T
# Plot
>>> odeplt(`ozzy.pdf`, time, ny, svars)
```

... or include the prebuilt integrator in you own script (like the crnsimulator exectuable):
```py
>>> from crnsimulator import get_integrator
>>> integrate = get_integrator(filename)
>>> integrate(args) # args = <argparse.ArgumentParser()>
```


## Installation
```sh
~$ python setup.py install
```
  
## Version
v0.9 -- code cleanup
  * removed networkx dependency
  * moved plotting libraries and functions into a separate file to avoid automatic import.

v0.8 -- beta status
  * now using logging
  * python >= 3.7 only
  * improved header documentation
  * using entry_points for crnsimulator script
  * set defaultrate = 1 (new postprocessing strandard)
  * new commandline arguments: labels, labels-strict
  * support the constant concentration flag

[oscillator.crn]: <https://github.com/bad-ants-fleet/crnsimulator/blob/master/tests/crns/oscillator.crn>
