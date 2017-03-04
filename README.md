# crnsimulator 

Translate chemical recation networks (CRNs) into ordinary differential
equations (ODEs) and integrate ODE systems.

## Examples
### Using the `crnsimulator` executable:

Create a test file with your CRN:

File: ozzy.crn
```
# Rock-Paper-Scissors Oscillator Test
A + B -> B + B [k = 0.2]
B + C -> C + C [k = 0.3]
C + A -> A + A [k = 1]
```

And pipe it into the crnsimulator:
```
$ crnsimulator -o ozzy < ozzy.crn
```
This writes the ODE system to an executable python script: `ozzy.py`

Check the commandline parameters of ozzy.py. You have to set initial species
concentrations, and choose an output-format, e.g.:
```
$ python ./ozzy.py --p0 A=0.1 B=1e-2 C=1e-3 --t8 10000 --pyplot ozzy.pdf
```
This example plots a simulation on a linear-time scale (0 - 10000) to the file `ozzy.pdf` .

### Tips when using the `crnsimulator` executable:

You can pass the commandline options for ozzy.py directly to `crnsimulator`.
This will automatically simulate your ODE system. Use --force to overwrite an
existing `ozzy.py` script.
```
$ crnsimulator --p0 A=0.1 B=1e-2 C=1e-3 --t8 10000 -o ozzy --pyplot ozzy.pdf < ozzy.crn
```

You can specify the CRN in a single line:

```
$ echo "A+B->2B [k=0.2]; B+C->2C [k=0.4]; C+A->2A" | crnsimulator --p0 A=0.1 B=1e-2 C=1e-3 --t8 10000 -o ozzy --pyplot ozzy.pdf
```

### Using the `crnsimulator` libary:

The easiest way to get started is by looking at the crnsimulator script itself.
However, here is a small example using the above Rock-Paper-Scissors oscillator.

```
>>> from crnsimulator import crn_to_ode, writeODElib
>>> name = 'ozzy'
>>> crn  = [[['A', 'B'],['B','B'],0.2],
            [['B', 'C'],['C','C'],0.8],
            [['C', 'A'],['A','A'],0.9]]
>>> svars, odes, jacobi, rdict = crn_to_ode(crn)
>>> olib = writeODElib(svars, odes, odename=name, jacobian=jacobi, rdict=rdict)
>>> print 'ODE system file:', olib  
ODE system file: ozzy.py
```

Then go ahead and execute `ozzy.py` or load it on-they-fly into your program.
```
$ python ./ozzy.py --p0 1=1e-6 2=2e-6 3=5e-6
```

## Installation
```
$ python setup.py install
```

### local installation
```
$ python setup.py install --user
```
  
## Version
0.1

## Complete list of Python dependencies:
All dependencies are available using `pip`:
  - os
  - sys
  - unittest
  - imp
  - argparse
  - pyparsing
  - networkx
  - numpy 
  - scipy
  - sympy
  - matplotlib
  - seaborn 

