#!/usr/bin/env python

# coded by: Stefan Badelt (badelt@caltech.edu)

# from __future__ import division, absolute_import, print_function, unicode_literals

import numpy as np
from scipy.integrate import odeint
from sympy import lambdify, sympify

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
sns.set_context("notebook", font_scale=1, rc={"lines.linewidth": 2.5})

from crnsimulator.sample_crns import oscillator, bin_counter
from crnsimulator.reactiongraph import crn_to_ode

def writeODElib(odename, var, func, rdict) :
  """ Write a python script that contains the ODE system.
  
  TODO: Add a function to execute the new script directly, 
  change parameters etc. (similar to SundialsWrapper)

  """
  # Print a python library that contains the ODE system.
  # both the initial concentration vector as well as rates
  odefile = odename + '.py'
  with open(odefile, 'w') as ofile :
    ofile.write("import numpy as np\n\n")
    #TODO: print default-rates into the file

    ofile.write("rates = {\n")
    for k in sorted(rdict.keys()):
      ofile.write("  '{}' : {},\n".format(k, rdict[k]))
  
    ofile.write("  }\n\n")

    # def myfunc(p0, t0, rates):
    ofile.write("def {}(p0, t0, r):\n".format(odename))

    # Initialize arguments
    ofile.write("  {} = p0\n".format(', '.join(sorted(var))))
    ofile.write("  if not r : r = rates\n\n")

    for k in sorted(rdict.keys()):
      ofile.write("  {} = r['{}']\n".format(k, k))

    # print the ODEs
    for i in range(len(var)):
      ofile.write("  d{}dt = {}\n".format(var[i], func[i]))
    ofile.write("\n")

    ofile.write("  return np.array([{}])\n".format(
      ', '.join(map(lambda x: 'd'+x+'dt', sorted(var)))))

  return True

def ode_plotter(name, t, ny, var, log=True):
  fig, ax = plt.subplots(1, 1, figsize=(7, 3.25))

  for e, y in enumerate(ny) :
    ax.plot(t, y, '-', label=var[e])

  ax.set_xlabel('Time [s]', fontsize=16)
  ax.set_ylabel('Conc. [M]', fontsize=16)
  if log :
    ax.set_xscale('log')

  plt.legend()
  fig.tight_layout()
  plt.savefig(name+'.pdf')

def sim_args():
  import argparse
  parser = argparse.ArgumentParser(
          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--p0", nargs='+', #default=['1=1'],
      help="Initial species concentration.")
  return parser.parse_args()

def get_crnsimulator_args(parser):
  """ A collection of arguments that are used by crnsimulator """

  parser.add_argument("--sample", default='oscillator',
      help="Import a CRN directly from crnsimulator.sample_crns")
  parser.add_argument("--nxy", action='store_true',
      help="Print time course in nxy format.")

  parser.add_argument("--p0", nargs='+', default=['1=1'],
      help="Initial species concentration.")
  parser.add_argument("--t0", type=float, default=1e-6,
      help="First time point of the printed time-course")
  parser.add_argument("--ti", type=float, default=1.02,
      help="Output-time increment of solver (t1 * ti = t2)")
  parser.add_argument("--t8", type=float, default=10000,
      help="Simulation time after transcription")

  return parser

def main():
  """Simulation of a CRN.
  """
  import argparse
  parser = argparse.ArgumentParser(
          formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser = get_crnsimulator_args(parser)

  args = parser.parse_args()

  # Input CRN:
  if args.sample == 'oscillator':
    crn = oscillator()
  elif args.sample == 'binary_counter':
    crn = binary_counter()
  else :
    raise Exception('Cannot find the sample CRN:', args.sample)


  if False :
    time = [0, args.t0]
    while time[-1] < args.t8 :
      time.append(time[-1]*args.ti)
  else :
    time = np.linspace(args.t0, args.t8, args.t8)

  ### => REACTIONGRAPH
  crn, ode, rdict = crn_to_ode(crn)

  ### => SYMPY
  var = []
  func = []
  for dx in sorted(ode.keys()):
    #print dx, '=', ' + '.join(['*'.join(map(str,xp)) for xp in ode[dx]])
    var.append(dx)
    func.append(sympify(' + '.join(['*'.join(map(str,xp)) for xp in ode[dx]])))

  p0 = [0] * len(var)

  if args.p0 :
    for term in args.p0:
      pos, val = term.split('=')
      p0[int(pos)-1] = float(val)
  else :
    p0[0] = 1

  print '#Initial population vector:', zip(var, p0)

  ### => SOLVER
  odename = 'oscillator'
  if writeODElib(odename, var, func, rdict) :
    #from odelib import odefunc
    _temp = __import__(odename, globals(), locals(), [], -1)
    odesystem = getattr(_temp, odename)

    # Set/Adjust Parameters
    rates = None # default rates from file
    ny = odeint(odesystem, p0, time, (rates, )).T

  if args.nxy:
    for i in zip(time, *ny):
      print ' '.join(map(str, i))

  ode_plotter(odename, time, ny, var, log=True)
  
if __name__ == '__main__':
  main()


