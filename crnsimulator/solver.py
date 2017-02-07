#!/usr/bin/env python

# coded by: Stefan Badelt (badelt@caltech.edu)

# from __future__ import division, absolute_import, print_function, unicode_literals

import imp # import from source on-the-fly
import argparse
import numpy as np
from scipy.integrate import odeint
from sympy import lambdify, sympify

import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set()
# sns.set_context("notebook", font_scale=1, rc={"lines.linewidth": 2.5})

from crnsimulator.sample_crns import oscillator, bin_counter
from crnsimulator.reactiongraph import crn_to_ode

def writeODElib(svars, odeM, odename='odesystem', jacobian=None, rdict=None, 
    concvect = [], template = None) :
  """ Write a python script that contains the ODE system.

  """
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
  functionstring += "  {} = p0\n".format(', '.join(svars))
  functionstring += "  if not r : r = rates\n\n"
  for k in sorted(rdict.keys()):
    functionstring += "  {} = r['{}']\n".format(k, k) 
  functionstring += "\n"
  ## Write the ODEs
  for i in range(len(svars)):
    functionstring += "  d{}dt = {}\n".format(svars[i], odeM[i]) 
  ## return
  functionstring += "  return np.array([{}])".format(
      ', '.join(map(lambda x: 'd'+x+'dt', svars)))
  odetemp = odetemp.replace("#<&>ODECALL<&>#",functionstring)

  if jacobian:
    # JACOBIAN FUNCTION
    jacobianstring = "def {}(p0, t0, r):\n".format('jacobian')
    ## Initialize arguments
    jacobianstring += "  {} = p0\n".format(', '.join(svars))
    jacobianstring += "  if not r : r = rates\n\n"
    for k in sorted(rdict.keys()):
      jacobianstring += "  {} = r['{}']\n".format(k, k) 
    jacobianstring += "\n"

    ## Write the jacobian
    jacobianstring += "  J = [[[] for i in range(len(p0))] " + \
        "for j in range(len(p0))]\n"

    vl = len(svars)
    i,j = 0,0
    for row in jacobian:
      jacobianstring += "  J[{}][{}] = {}\n".format(i, j, row)
      if j < vl-1 :
        j += 1
      else :
        i += 1
        j = 0
    ## return
    jacobianstring += "  return J"
    odetemp = odetemp.replace("#<&>JACOBIAN<&>#",jacobianstring)
    odetemp = odetemp.replace("#<&>JCALL<&>#",'Dfun = jacobian')

  # SORTED VARIABLE NAMES in integrate()
  svarstring = 'svars = ' + '[{}]'.format(
      ', '.join(map(lambda x: str('"'+x+'"'), svars)))
  odetemp = odetemp.replace("#<&>SORTEDVARS<&>#",svarstring)

  # Default concentrations in integrate()
  concstring = ''
  #print "\n  ".join([map("p0[{}] = {}".format, enumerate(concvect))])
  for e, c in enumerate(concvect) :
    if c :
      concstring += "p0[{}] = {}\n  ".format(e,c)
  odetemp = odetemp.replace("#<&>DEFAULTCONCENTRATIONS<&>#",concstring)

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
  plt.savefig(name)
  return name

def add_integrator_args(parser):
  """Simulation Aruments """
  # scipy.integrate.odeint parameters
  parser.add_argument("-a", "--atol", type=float, default=None,
      help="Specify absolute tolerance for the solver.")
  parser.add_argument("-r", "--rtol", type=float, default=None,
      help="Specify relative tolerance for the solver.")
  parser.add_argument("--mxstep", type=int, default=0,
      help="Maximum number of steps allowed for each integration point in t.")

  # crn parameters
  parser.add_argument("--p0", nargs='+', #default=['1=1'],
      help="Initial species concentration.")
  parser.add_argument("--rates", default=None,
      help="*not implemented*, using default for now!")

  # simulation time
  parser.add_argument("--t0", type=float, default=0.1,
      help="First time point of the printed time-course.")
  parser.add_argument("--ti", type=float, default=1.02,
      help="Output-time increment of solver (t1 * ti = t2).")
  parser.add_argument("--t8", type=float, default=1000,
      help="Simulation time.")

  # output format
  parser.add_argument("--name", default='crn_simulation',
      help="Name the plot outputfile.")
  parser.add_argument("--noplot", action='store_true',
      help="Do *not* plot the simulation using matplotlib.")
  parser.add_argument("--nxy", action='store_true',
      help="Print time course in nxy format.")
  #parser.add_argument("--verbose", action='store_true',
  #    help="Print more information.")
  return

def main():
  """ On-the-fly simulation of a CRN. """
  parser = argparse.ArgumentParser(
          formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument("--sample", default='oscillator',
      help="Import a CRN directly from crnsimulator.sample_crns")

  add_integrator_args(parser)

  args = parser.parse_args()

  # Input CRN:
  if args.sample == 'oscillator':
    crn = oscillator()
  elif args.sample == 'binary_counter':
    crn = binary_counter()
  else :
    raise Exception('Cannot find the sample CRN:', args.sample)

  #TODO(SB): CMD options?
  if False :
    time = [0, args.t0]
    while time[-1] < args.t8 :
      time.append(time[-1]*args.ti)
  else :
    time = np.linspace(args.t0, args.t8, args.t8)

  if args.name == 'crn_simulation' and args.sample:
    odename = args.sample
  else :
    odename = args.name

  ### => REACTIONGRAPH
  svars, M, J, R = crn_to_ode(crn)

  if not args.p0 :
    for e, v in enumerate(svars, 1) :
      print e, v
    raise SystemExit('please specify the initial concentration vector' + \
        'with --p0, e.g.: --p0 1=1 2=0.005 3=1e-5')
  else :
    p0 = [0] * len(svars)
    for term in args.p0 :
      p,o = term.split('=')
      p0[int(p)-1] = float(o)
  print '# Initial concentrations:', zip(svars,p0)

  ### => SOLVER
  odefile =  writeODElib(svars, M, odename=odename, jacobian=J, rdict=R)
  print '# Wrote ODE system:', odefile
  _temp = imp.load_source(odename, "./"+odefile)

  odesystem = getattr(_temp, odename)
  if J :
    jacobian = getattr(_temp, 'jacobian')
  else :
    jacobian = None

  # Set/Adjust Parameters
  rates = None
  ny = odeint(odesystem, p0, time, (rates, ), 
      Dfun=jacobian, rtol=args.rtol, atol=args.atol, mxstep=args.mxstep).T

  if args.nxy :
    for i in zip(time, *ny):
      print ' '.join(map("{:.9e}".format, i))

  if not args.noplot :
    plotfile = ode_plotter(odename+'.pdf', time, ny, svars, log=False)
    print '# Printed file:', plotfile
  
if __name__ == '__main__':
  main()


