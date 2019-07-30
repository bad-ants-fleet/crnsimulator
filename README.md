# crnsimulator 

Simulate chemical recation networks (CRNs) using ordinary differential
equations (ODEs).

## Examples
### Using the `crnsimulator` executable:

Create a test file with your CRN:

File: ozzy.crn
```
# Oscillator Test
A + B -> B + B [k = 0.2]
B + C -> C + C [k = 0.3]
C + A -> A + A [k = 1]
```

And pipe it into the crnsimulator:
```sh
~$ crnsimulator -o ozzy < ozzy.crn
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
~$ crnsimulator --p0 A=0.1 B=1e-2 C=1e-3 --t8 10000 -o ozzy --pyplot ozzy.pdf < ozzy.crn
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
>>> filename, odename = RG.write_ODE_lib(filename='ozzy.py')
>>> print('Wrote ODE system file:', filename)
Wrote ODE system file: ozzy.py
```

Then go ahead and execute `ozzy.py`
```sh
~$ python ./ozzy.py --p0 1=1e-6 2=2e-6 3=5e-6 --t8 1e8 --pyplot ozzy.pdf
```

... or load it as python library.

```py
>>> from crnsimulator import get_integrator
>>> integrate = get_integrator(odename, filename)
>>> integrate(args) # args = <argparse.ArgumentParser()>
```


## Installation
```sh
~$ python setup.py install
```

### local installation
```sh
~$ python setup.py install --user
```
  
## Version
0.6

