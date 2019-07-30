from __future__ import unicode_literals

import os
import unittest
from argparse import ArgumentParser

from crnsimulator import get_integrator
from crnsimulator.reactiongraph import ReactionGraph, ReactionNode
from crnsimulator.crn_parser import parse_crn_string
from crnsimulator.odelib_template import add_integrator_args


class testSolver(unittest.TestCase):
    def setUp(self):
        parser = ArgumentParser()
        add_integrator_args(parser)
        self.args = parser.parse_args([])
        self.filename = 'test_file.py'
        self.executable = 'test_file.pyc'

    def tearDown(self):
        ReactionNode.rid = 0
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.executable):
            os.remove(self.executable)

    def test_crn(self):
        # At some pont the simulator had troubles with CRNs that have
        # only one species...
        crn = "2X <=> 3X; X -> [k=0.1]"
        crn, _ = parse_crn_string(crn, process=True)

        # Split CRN into irreversible reactions
        new = []
        for [r, p, k] in crn:
            if None in k:
                k[:] = [x if x is not None else 1 for x in k]
            if len(k) == 2:
                new.append([r, p, k[0]])
                new.append([p, r, k[1]])
            else:
                new.append([r, p, k[0]])
        crn = new

        RG = ReactionGraph(crn)

        filename, odename = RG.write_ODE_lib(filename=self.filename)
        integrate = get_integrator(odename, filename)

        self.args.p0 = ['1=0.5']
        self.args.t_log = 10
        self.args.t0 = 0.1
        self.args.t8 = 10
        simu = list(integrate(self.args))

        first = simu[0]
        last = simu[-1]

        self.assertEqual(first, (0.10000000000000001, 0.5))
        self.assertEqual(last, (10.0, 0.88535344232897151))

    def test_crn_sympy_imports(self):
        # Test if the simulator can handle awkward species names:
        # From sympy.sympify: If you want all single-letter and Greek-letter
        # variables to be symbols then you can use the clashing-symbols
        # dictionaries that have been defined there as private variables: _clash1
        # (single-letter variables), _clash2 (the multi-letter Greek names) or
        # _clash (both single and multi-letter names that are defined in abc).
        crn = "2S <=> 3sin; sin + cos -> A; S -> cos [k=0.1]"
        crn, _ = parse_crn_string(crn, process=True)

        # Split CRN into irreversible reactions
        new = []
        for [r, p, k] in crn:
            if None in k:
                k[:] = [x if x is not None else 1 for x in k]
            if len(k) == 2:
                new.append([r, p, k[0]])
                new.append([p, r, k[1]])
            else:
                new.append([r, p, k[0]])
        crn = new

        RG = ReactionGraph(crn)

        filename, odename = RG.write_ODE_lib(filename=self.filename)
        integrate = get_integrator(odename, filename)

        self.args.p0 = ['S=0.5', 'cos=0.2']
        self.args.t_log = 10
        self.args.t0 = 0.1
        self.args.t8 = 10
        simu = list(integrate(self.args))

        first = simu[0]
        last = simu[-1]

        self.assertEqual(first, (0.10, 0.0, 0.5, 0.20, 0.0))
        self.assertEqual(
            last,
            (10.0,
             0.27442495177208459,
             0.06646052036496547,
             0.068597456334669946,
             0.16135065552033576))
