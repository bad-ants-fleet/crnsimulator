#!/usr/bin/env python3
"""
Simulate formal Chemical Reaction Networks using ODEs (executable).

Usage:
    simulator.py --help
"""
import logging
logger = logging.getLogger(__name__)

import re
import os
import sys
import argparse

from crnsimulator import __version__
from crnsimulator import ReactionGraph, get_integrator, parse_crn_string
from crnsimulator.odelib_template import add_integrator_args
from crnsimulator.crn_parser import ParseException

class SimulationSetupError(Exception):
    pass

def natural_sort(l):
    """
    Sorts a collection in the order humans would expect. Implementation from
    http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
    """
    def convert(text): 
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): 
        return [convert(c) for c in re.split('([0-9]+)', str(key))]

    return sorted(l, key=alphanum_key)

def main():
    """Translate a CRN into an ODE system. 

    Optional: Simulate ODEs on-the-fly.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument("-v", "--verbose", action='count', default = 0,
        help = "Print logging output. (-vv increases verbosity.)")
    parser.add_argument('--logfile', default = '', action = 'store', metavar = '<str>',
        help = """Redirect logging information to a file.""")
    parser.add_argument("--force", action='store_true',
            help="Overwrite existing files")
    parser.add_argument("--dryrun", action='store_true',
            help="Do not run the simulation, only write the files.")
    parser.add_argument("-o", "--output", default='odesystem', metavar='<str>',
            help="Name of ODE library files.")
    parser.add_argument("--no-jacobian", action='store_true',
            help=argparse.SUPPRESS)
    parser.add_argument("--jacobian", action='store_true',
            help="""Symbolic calculation of Jacobi-Matrix. 
            This may generate a very large simulation file.""")
    add_integrator_args(parser)
    args = parser.parse_args()

    # ~~~~~~~~~~~~~
    # Logging Setup 
    # ~~~~~~~~~~~~~
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(args.logfile) if args.logfile else logging.StreamHandler()
    if args.verbose == 0:
        handler.setLevel(logging.WARNING)
    elif args.verbose == 1:
        handler.setLevel(logging.INFO)
    elif args.verbose == 2:
        handler.setLevel(logging.DEBUG)
    elif args.verbose >= 3:
        handler.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if args.no_jacobian:
        logger.warning('Deprecated argument: --no-jacobian.')
    if args.pyplot_labels:
        logger.warning('Deprecated argument: --pyplot_labels.')
        args.labels = args.pyplot_labels
        args.pyplot_labels = None

    # ********************* #
    # ARGUMENT PROCESSING 1 #
    # ..................... #
    filename = args.output + \
        '.py' if args.output[-3:] != '.py' else args.output
    odename = 'odesystem'

    input_crn = sys.stdin.readlines()
    input_crn = "".join(input_crn)

    try:
        crn, species = parse_crn_string(input_crn)
    except ParseException as ex:
        logger.error('CRN-format parsing error:')
        logger.error('Cannot parse line {:5d}: "{}"'.format(ex.lineno, ex.line))
        logger.error('                          {} '.format(' ' * (ex.col-1) + '^'))
        raise SystemExit

    V = [] # sorted species (vertices) vector
    C = [] # corresponding concentration vector
    seen = set() # keep track of what species are covered

    # Move interesting species to the front, in the given order.
    labels = args.labels
    for s in labels:
        if s in seen :
            raise SimulationSetupError(f'Multiple occurances of {s} in labels.')
        V.append(s)

        if species[s][0][0] != 'i': 
            raise NotImplementedError('Concentrations must be given as "initial" concentrations.')
        C.append(species[s][1])
        seen.add(s)

    # Append the remaining specified species 
    for s in natural_sort(species):
        if s in seen : continue
        V.append(s)
        if species[s][0][0] != 'i':
            raise NotImplementedError('Concentrations must be given as "initial" concentrations.')
        C.append(species[s][1])
        seen.add(s)

    # Split CRN into irreversible reactions
    new = []
    for [r, p, k] in crn:
        if None in k:
            logger.error('Rate == None. This should not happen with the new default parameters.')
            k[:] = [x if x is not None else 1 for x in k]

        if len(k) == 2:
            new.append([r, p, k[0]])
            new.append([p, r, k[1]])
        else:
            new.append([r, p, k[0]])
    crn = new

    # **************** #
    # WRITE ODE SYSTEM #
    # ................ #
    if not args.force and os.path.exists(filename):
        logger.warning(f'Reading ODE system from existing file: {filename}')
    else:
        # ******************* #
        # BUILD REACTIONGRAPH #
        # ................... #
        RG = ReactionGraph(crn)
        if len(RG.species) != len(V):
            logger.error(f'Species input: ({len(V)}): {sorted(V)}')
            logger.error(f'Species in CRN: ({len(RG.species)}): {sorted(RG.species)}')
            raise SimulationSetupError('Confusion about which species appear in the reaction network!')

        # ********************* #
        # PRINT ODE TO TEMPLATE #
        # ..................... #
        filename, odename = RG.write_ODE_lib(sorted_vars = V, concvect = C,
                                             jacobian = args.jacobian, 
                                             filename = filename,
                                             odename = odename)
        logger.info(f'CRN to ODE translation successful. Wrote file: {filename}')

    # ******************* #
    # SIMULATE ODE SYSTEM #
    # ................... #
    if args.dryrun:
        logger.info('Dryrun: Simulate the ODE system using:')
        logger.info(f"  python {filename} --help ")
    else:
        logger.info('Simulating the ODE system, change parameters using:')
        logger.info(f"  python {filename} --help ")

        integrate = get_integrator(filename)

        # ********************* #
        # ARGUMENT PROCESSING 2 #
        # ..................... #
        integrate(args, setlogger = True)

    return


if __name__ == '__main__':
    main()

