# crnsimulator

The CRNsimulator translates a chemical recation network (CRN) into a set of
ordinary differential equations, (ODEs), writes these equations into a new
Python library file and then integrates the ODE system.

### Requires:
  - networkx
  - numpy 
  - scipy
  - sympy
  - matplotlib
  - seaborn

## Example:

```
./crnsimulator --import_sample oscillator --name ossi --t0 1e-8 --t8 1e10 --ti 1.02
```

This will produce two files: `ossi.py` is a temporary file that contains the
ODE system in form of a python script. `ossi.pdf` is a plot of the simulation.

