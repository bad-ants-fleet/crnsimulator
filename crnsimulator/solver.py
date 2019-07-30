#
# CRN-to-MultiDiGraph-to-ODE translation utilities.
#
# Written by Stefan Badelt (badelt@caltech.edu).
#
# Use at your own risk.
#

from builtins import map
from builtins import str
from builtins import range
import crnsimulator.odelib_template

def get_integrator(odename, filename):
    """Workaround to avoid deprecation warnings for the imp module.
    """
    try: # Python 3.7
        import types
        import importlib.machinery

        loader = importlib.machinery.SourceFileLoader(odename, filename)
        mod = types.ModuleType(loader.name)
        loader.exec_module(mod)

        return getattr(mod, 'integrate')
    except ImportError as err: # Python 2.7
        import imp
        _temp = imp.load_source(odename, filename)
        return getattr(_temp, 'integrate')

def writeODElib(svars, odeM, jacobian=None, rdict=None, concvect=None,
                odename='odesystem', filename='./odesystem', template=None):
    """ Write an ODE system into an executable python script.

    Args:
      svars <list[str]>: Sorted list of variables. The sorting defines the order
        for specifying concentrations.
      odeM <sympy.Matrix()>: A matrix that contains the ODE system.
      jacobian <optional: sympy.Matrix()> : The jacobi Matrix corresponding to
        odeM.
      rdict <optional: dict()>: If your odeM contains rates in form of variable
        names, then you need to supply this dictionary mapping names to float values.
      concvect <optional: list(): Specify default initial species concentrations
        in the order defined by svars.
      odename <optional: str>: Name of your ODE function (no special characters!)
      filename <optional: str>: Specify the name of the ODE library.
      template <optional: str>: Specify an alternative template library file.

    Returns:
      filename<str>, odename<str>

    """
    if not template:
        template = crnsimulator.odelib_template.__file__[:]
        if template[-1] == 'c':
            template = template[:-1]

    svars = list(map(str, svars))

    odetemp = ''
    with open(template, 'r') as tfile:
        odetemp = tfile.read()

    # REPLACE NAMES
    odetemp = odetemp.replace("#<&>ODENAME<&>#", odename)
    odetemp = odetemp.replace("#<&>FILENAME<&>#", filename)

    # DEFAULT RATES
    ratestring = ',\n'.join(
        "  '{}' : {}".format(k, rdict[k]) for k in sorted(rdict.keys()))
    odetemp = odetemp.replace("#<&>RATES<&>#", ratestring)

    # ODEINT FUNCTION
    functionstring = "def {}(p0, t0, r):\n".format(odename)
    # Initialize arguments
    functionstring += "    {} = p0\n".format(', '.join(svars))
    functionstring += "    if not r : r = rates\n\n"
    for k in sorted(rdict.keys()):
        functionstring += "    {} = r['{}']\n".format(k, k)
    functionstring += "\n"
    # Write the ODEs
    for i in range(len(svars)):
        functionstring += "    d{}dt = {}\n".format(svars[i], odeM[i])
    # return
    if len(svars) == 1:
        functionstring += "    return np.array({})".format(
            ', '.join(['d' + x + 'dt' for x in svars]))
    else:
        functionstring += "    return np.array([{}])".format(
            ', '.join(['d' + x + 'dt' for x in svars]))
    odetemp = odetemp.replace("#<&>ODECALL<&>#", functionstring)

    if jacobian:
        # JACOBIAN FUNCTION
        jacobianstring = "def {}(p0, t0, r):\n".format('jacobian')
        # Initialize arguments
        jacobianstring += "    {} = p0\n".format(', '.join(svars))
        jacobianstring += "    if not r : r = rates\n\n"
        for k in sorted(rdict.keys()):
            jacobianstring += "    {} = r['{}']\n".format(k, k)
        jacobianstring += "\n"

        # Write the jacobian
        jacobianstring += "    J = [[[] for i in range(len(p0))] " + \
            "for j in range(len(p0))]\n"

        vl = len(svars)
        i, j = 0, 0
        for row in jacobian:
            jacobianstring += "    J[{}][{}] = {}\n".format(i, j, row)
            if j < vl - 1:
                j += 1
            else:
                i += 1
                j = 0

        if len(svars) == 1:
            jacobianstring += "    J = J[0]\n"

        # return
        jacobianstring += "    return J"
        odetemp = odetemp.replace("#<&>JACOBIAN<&>#", jacobianstring)
        odetemp = odetemp.replace("#<&>JCALL<&>#", 'Dfun = jacobian')

    # SORTED VARIABLE NAMES in integrate()
    svarstring = 'svars = ' + '[{}]'.format(
        ', '.join([str('"' + x + '"') for x in svars]))
    odetemp = odetemp.replace("#<&>SORTEDVARS<&>#", svarstring)

    # Default concentrations in integrate()
    concstring = ''

    if concvect:
        for e, c in enumerate(concvect):
            if c:
                concstring += "p0[{}] = {}\n    ".format(e, c)
    odetemp = odetemp.replace("#<&>DEFAULTCONCENTRATIONS<&>#", concstring)

    if filename[-3:] != '.py':
        filename += '.py'
    with open(filename, 'w') as ofile:
        ofile.write(odetemp)

    return filename, odename
