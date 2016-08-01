#!/usr/bin/env python

# coded by: Stefan Badelt (badelt@caltech.edu)

# from __future__ import division, absolute_import, print_function, unicode_literals

import argparse
import numpy as np
from scipy.integrate import odeint
from sympy import lambdify, sympify

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
sns.set_context("notebook", font_scale=1, rc={"lines.linewidth": 2.5})

from crnsimulator.sample_crns import oscillator, bin_counter
from crnsimulator.reactiongraph import crn_to_ode

def writeODElib(odename, odedict, rdict, svars = None, template = None) :
  """ Write a python script that contains the ODE system.
  

  """
  if svars :
    assert len(svars) == len(odedict.keys())
  else :
    svars = sorted(odedict.keys())

  if not template :
    import crnsimulator.odelib_template
    template = crnsimulator.odelib_template.__file__[:-1]

  odetemp = ''
  with open(template, 'r') as tfile:
    odetemp = tfile.read()

  # REPLACE NAMES
  odetemp = odetemp.replace("#<&>ODENAME<&>#",odename)

  # DEFAULT RATES
  ratestring = ',\n'.join(
      "  '{}' : {}".format(k, rdict[k]) for k in sorted(rdict.keys()))
  odetemp = odetemp.replace("#<&>RATES<&>#",ratestring)

  # ODEINT FUNCTION
  functionstring =  "def {}(p0, t0, r):\n".format(odename)
  ## Initialize arguments
  functionstring += "  {} = p0\n".format(', '.join(sorted(svars)))
  functionstring += "  if not r : r = rates\n\n"
  for k in sorted(rdict.keys()):
    functionstring += "  {} = r['{}']\n".format(k, k) 
  functionstring += "\n"
  ## Write the ODEs
  for i in range(len(svars)):
    functionstring += "  d{}dt = {}\n".format(svars[i], odedict[svars[i]]) 
  ## return
  functionstring += "  return np.array([{}])".format(
      ', '.join(map(lambda x: 'd'+x+'dt', sorted(svars))))
  odetemp = odetemp.replace("#<&>ODECALL<&>#",functionstring)

  # SORTED VARIABLE NAMES in integrate()
  svarstring = 'svars = ' + '[{}]'.format(
      ', '.join(map(lambda x: str('"'+x+'"'), sorted(svars))))
  odetemp = odetemp.replace("#<&>SORTEDVARS<&>#",svarstring)

  odefile = odename + '.py'
  with open(odefile,'w') as ofile :
    ofile.write(odetemp)

  return odefile

def ode_plotter(name, t, ny, svars, log=True):
  fig, ax = plt.subplots(1, 1, figsize=(7, 3.25))

  for e, y in enumerate(ny) :
    ax.plot(t, y, '-', label=svars[e])

  ax.set_xlabel('Time [s]', fontsize=16)
  ax.set_ylabel('Conc. [M]', fontsize=16)
  if log :
    ax.set_xscale('log')
  else :
    ax.set_xscale('linear')

  plt.legend()
  fig.tight_layout()
  plt.savefig(name+'.pdf')

def get_crnsimulator_args(parser):
  """ A collection of arguments that are used by crnsimulator """

  parser.add_argument("--sample", default='oscillator',
      help="Import a CRN directly from crnsimulator.sample_crns")
  parser.add_argument("--nxy", action='store_true',
      help="Print time course in nxy format.")

  parser.add_argument("--p0", nargs='+', default=['1=1'],
      help="Initial species concentration.")
  parser.add_argument("--t0", type=float, default=0.1,
      help="First time point of the printed time-course")
  parser.add_argument("--ti", type=float, default=1.02,
      help="Output-time increment of solver (t1 * ti = t2)")
  parser.add_argument("--t8", type=float, default=10000,
      help="Simulation time after transcription")
  return parser

def main():
  """ On-the-fly simulation of a CRN. """
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
  odict, rdict = crn_to_ode(crn, rate_dict = True, symplification = True)

  svars = sorted(odict.keys())

  if not args.p0 :
    for e, v in enumerate(svars, 1) :
      print e, v
    raise SystemExit('please specify the initial concentration vector' + \
        'with --p0, e.g.: --p0 1=1 --p0 2=0.005 3=1e-6')
  else :
    p0 = [0] * len(svars)
    for term in args.p0 :
      p,o = term.split('=')
      p0[int(p)-1] = float(o)
  print '# Initial concentrations:', zip(svars,p0)

  ### => SOLVER
  odename = 'oscillator'
  if writeODElib(odename, odict, rdict, svars=svars) :
    _temp = __import__(odename, globals(), locals(), [], -1)
    odesystem = getattr(_temp, odename)

    # Set/Adjust Parameters
    rates = None # default rates from file
    ny = odeint(odesystem, p0, time, (rates, )).T

  if args.nxy :
    for i in zip(time, *ny):
      print ' '.join(map("{:.9e}".format, i))

  ode_plotter(odename, time, ny, svars, log=False)
  
if __name__ == '__main__':
  main()


