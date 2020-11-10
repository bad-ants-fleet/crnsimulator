#!/usr/bin/env python
"""
A template file to simulate a specific system of Ordinary Differential Equations (ODEs).

... or an autogenerated script from the *crnsimulator* Python package.

Note: If this file is executable, it is *autogenerated*.
    This means it contains a system of hardcoded ODEs together with some
    default parameters. While it may be tempting to tweak some functions,
    beware that this file may be overwritten by the next execution of the
    `crnsimulator` executable.  Edits should be done at the source file:
    "crnsimulator.odelib_template.py" or you can provide an alternative
    template file. Use the option --output to avoid overwriting this file.

Usage: 
    python #<&>FILENAME<&># --help
"""

import logging
logger = logging.getLogger(__name__)

import argparse
import numpy as np
from scipy.integrate import odeint

class ODETemplateError(Exception):
    pass

rates = {
    #<&>RATES<&>#
}

#<&>ODECALL<&>#

#<&>JACOBIAN<&>#


def add_integrator_args(parser):
    """ODE integration aruments."""
    solver = parser.add_argument_group('odeint parameters')
    plotter = parser.add_argument_group('plotting parameters')

    # required: simulation time and output settings
    solver.add_argument("--t0", type=float, default=0, metavar='<flt>',
            help="First time point of the time-course.")
    solver.add_argument("--t8", type=float, default=100, metavar='<flt>',
            help="End point of simulation time.")
    plotter.add_argument("--t-lin", type=int, default=500, metavar='<int>',
            help="Returns --t-lin evenly spaced numbers on a linear scale from --t0 to --t8.")
    plotter.add_argument("--t-log", type=int, default=None, metavar='<int>',
            help="Returns --t-log evenly spaced numbers on a logarithmic scale from --t0 to --t8.")

    # required: initial concentration vector
    solver.add_argument("--p0", nargs='+', metavar='<int/str>=<flt>',
            help="""Vector of initial species concentrations. 
            E.g. \"--p0 1=0.5 3=0.7\" stands for 1st species at a concentration of 0.5 
            and 3rd species at a concentration of 0.7. You may chose to address species
            directly by name, e.g.: --p0 C=0.5.""")
    # advanced: scipy.integrate.odeint parameters
    solver.add_argument("-a", "--atol", type=float, default=None, metavar='<flt>',
            help="Specify absolute tolerance for the solver.")
    solver.add_argument("-r", "--rtol", type=float, default=None, metavar='<flt>',
            help="Specify relative tolerance for the solver.")
    solver.add_argument("--mxstep", type=int, default=0, metavar='<int>',
            help="Maximum number of steps allowed for each integration point in t.")

    # optional: choose output formats
    plotter.add_argument("--list-labels", action='store_true',
            help="Print all species and exit.")
    plotter.add_argument("--labels", nargs='+', default=[], metavar='<str>+',
            help="""Specify the (order of) species which should appear in the pyplot legend, 
            as well as the order of species for nxy output format.""")
    plotter.add_argument("--labels-strict", action='store_true',
            help="""When using pyplot, only plot tracjectories corresponding to labels,
            when using nxy, only print the trajectories corresponding to labels.""")
 
    plotter.add_argument("--nxy", action='store_true',
            help="Print time course to STDOUT in nxy format.")
    plotter.add_argument("--header", action='store_true',
            help="Print header for trajectories.")

    plotter.add_argument("--pyplot", default='', metavar='<str>',
            help="Specify a filename to plot the ODE simulation.")
    plotter.add_argument("--pyplot-xlim", nargs=2, type=float, default=None, metavar='<flt>',
            help="Specify the limits of the x-axis.")
    plotter.add_argument("--pyplot-ylim", nargs=2, type=float, default=None, metavar='<flt>',
            help="Specify the limits of the y-axis.")
    plotter.add_argument("--pyplot-labels", nargs='+', default=[], metavar='<str>+',
            help=argparse.SUPPRESS)
    return

def flint(inp):
    return int(inp) if float(inp) == int(float(inp)) else float(inp)

def set_logger(verbose, logfile):
    # ~~~~~~~~~~~~~
    # Logging Setup 
    # ~~~~~~~~~~~~~
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(logfile) if logfile else logging.StreamHandler()
    if verbose == 0:
        handler.setLevel(logging.WARNING)
    elif verbose == 1:
        handler.setLevel(logging.INFO)
    elif verbose == 2:
        handler.setLevel(logging.DEBUG)
    elif verbose >= 3:
        handler.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def integrate(args, setlogger = False):
    """Main interface to solve the ODE-system.

    Args:
      args (:obj:`argparse.ArgumentParser()`): An argparse object containing all of
        the arguments of :obj:`crnsimulator.add_integrator_args()`.

    Prints:
      - plot files
      - time-course

    Returns:
      Nothing
    """
    if setlogger:
        set_logger(args.verbose, args.logfile)

    if args.pyplot_labels:
        logger.warning('Deprecated argument: --pyplot_labels.')

    #<&>SORTEDVARS<&>#

    p0 = [0] * len(svars)
    #<&>DEFAULTCONCENTRATIONS<&>#
    const = None
    #<&>CONSTANT_SPECIES_INFO<&>#
    if args.p0:
        for term in args.p0:
            p, o = term.split('=')
            try:
                pi = svars.index(p)
            except ValueError as e:
                pi = int(p) - 1
            finally:
                p0[pi] = flint(o)
    else:
        msg = 'Specify a vector of initial concentrations: ' + \
                'e.g. --p0 1=0.1 2=0.005 3=1e-6 (see --help)'
        if sum(p0) == 0:
            logger.warning(msg)
            args.list_labels = True
        else:
            logger.info(msg)

    if args.list_labels:
        print('List of variables and initial concentrations:')
        for e, v in enumerate(svars, 1):
            if args.labels_strict and e > len(args.labels):
                break
            print(f'{e} {v} {p0[e-1]} {"constant" if const and const[e-1] else ""}')
        raise SystemExit('Initial concentrations can be overwritten by --p0 argument')

    if not args.nxy and not args.pyplot:
        logger.warning('Use --pyplot and/or --nxy to plot your results.')

    if not args.t8:
        raise ODETemplateError('Specify a valid end-time for the simulation: --t8 <flt>')

    if args.t_log:
        if args.t0 == 0:
            raise ODETemplateError('--t0 cannot be 0 when using log-scale!')
        time = np.logspace(np.log10(args.t0), np.log10(args.t8), num=args.t_log)
    elif args.t_lin:
        time = np.linspace(args.t0, args.t8, num=args.t_lin)
    else:
        raise ODETemplateError('Please specify either --t-lin or --t-log. (see --help)')

    # It would be nice if it is possible to read alternative rates from a file instead.
    # None triggers the default-rates that are hard-coded in the (this) library file.
    rates = None

    logger.info(f'Initial concentrations: {list(zip(svars, p0))}')
    # TODO: logging should report more info on parameters.

    ny = odeint(#<&>ODENAME<&>#,
        np.array(p0), time, (rates, ), #<&>JCALL<&>#,
        atol=args.atol, rtol=args.rtol, mxstep=args.mxstep).T

    # Output
    if args.nxy and args.labels_strict:
        end = len(args.labels)
        if args.header:
            print(' '.join(['{:15s}'.format(x) for x in ['time'] + svars[:end]]))
        for i in zip(time, *ny[:end]):
            print(' '.join(map("{:.9e}".format, i)))
    elif args.nxy:
        if args.header:
            print(' '.join(['{:15s}'.format(x) for x in ['time'] + svars]))
        for i in zip(time, *ny):
            print(' '.join(map("{:.9e}".format, i)))

    if args.pyplot:
        from crnsimulator.plotting import ode_plotter
        plotfile = ode_plotter(args.pyplot, time, ny, svars,
                               log=True if args.t_log else False,
                               labels=set(args.labels),
                               xlim = args.pyplot_xlim,
                               ylim = args.pyplot_ylim,
                               labels_strict = args.labels_strict)
        logger.info(f"Plotting successfull. Wrote plot to file: {plotfile}")

    return zip(time, *ny)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--verbose", action='count', default = 0,
        help = "Print logging output. (-vv increases verbosity.)")
    parser.add_argument('--logfile', default = '', action = 'store', metavar = '<str>',
        help = """Redirect logging information to a file.""")
    add_integrator_args(parser)
    args = parser.parse_args()
    integrate(args, setlogger = True)

