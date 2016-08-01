# crnsimulator

The CRNsimulator translates a chemical recation network (CRN) into a set of
ordinary differential equations, (ODEs), writes these equations into a new
Python library file and then integrates the ODE system.

## Examples:
### Using the `crnsimulator` executable:

```
./crnsimulator --import_sample oscillator --name ozzy --t0 1e-8 --t8 1e10 --ti 1.02
```

This will produce two files: `ozzy.py` is a temporary file that contains the
ODE system in form of a python script. `ozzy.pdf` is a plot of the simulation.

### Using the `crnsimulator` libary:

```
>>> from crnsimulator import crn_to_ode, writeODElib
>>> name = 'ozzy'
>>> crn  = [[['A', 'B'],['B','B'],0.2],
            [['B', 'C'],['C','C'],0.8],
            [['C', 'A'],['A','A'],0.9]]
>>> svars, odes, jacobi, rdict = crn_to_ode(crn)
>>> olib = writeODElib(name, svars, odes, jacobi, rdict)
>>> print 'ODE system file:', olib
```

The ODE-system-file can be directly executed, e.g. with:
```
python ./ozzy.py --p0 1=1e-6 2=2e-6 3=5e-6
```

## Python dependencies:
  - networkx
  - numpy 
  - scipy
  - sympy
  - matplotlib
  - seaborn

