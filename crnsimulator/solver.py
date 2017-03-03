#
# CRN-to-MultiDiGraph-to-ODE translation utilities.
# 
# Written by Stefan Badelt (badelt@caltech.edu).
#
# Use at your own risk. 
#
#

import os
import imp # import from source on-the-fly
import argparse

def writeODElib(svars, odeM, jacobian=None, rdict=None, 
    odename = 'odesystem', path = './', concvect = [], template = None) :
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

  odefile = path + '/' + odename + '.py'
  with open(odefile,'w') as ofile :
    ofile.write(odetemp)

  return odefile

