#
# Unittests for crnsimulator.reactiongraph
#
# Written by Stefan Badelt (badelt@caltech.edu).
#

import unittest
from crnsimulator.reactiongraph import ReactionGraph, ReactionNode


class Test_ReactionGraph(unittest.TestCase):
    def setUp(self):
        self.backup = ReactionNode.rid
        ReactionNode.rid = 0

    def tearDown(self):
        ReactionNode.rid = self.backup

    def test_init_from_crn(self):
        crn = [[['A', 'B', 'B'], ['C'], 5]]
        RG = ReactionGraph(crn)
        self.assertIsInstance(RG, ReactionGraph)
        self.assertEqual(sorted(RG.species), ['A', 'B', 'C'])
        self.assertEqual(sorted(RG.reactants), ['A', 'B'])
        self.assertEqual(sorted(RG.products), ['C'])

        crn = [[['A', 'B'], ['C'], 18], [['A'], ['C', 'E'], 99]]
        RG = ReactionGraph(crn)
        self.assertEqual(sorted(RG.species), ['A', 'B', 'C', 'E'])
        self.assertEqual(sorted(RG.reactants), ['A', 'B'])
        self.assertEqual(sorted(RG.products), ['C', 'E'])

        crn = [[['A', 'B', 'B'], ['C'], [5]]]
        RG = ReactionGraph(crn)
        self.assertIsInstance(RG, ReactionGraph)
        self.assertEqual(sorted(RG.species), ['A', 'B', 'C'])
        self.assertEqual(sorted(RG.reactants), ['A', 'B'])
        self.assertEqual(sorted(RG.products), ['C'])

        # TODO: structure of M and R is variable, cannot check it like this
        # M, R = RG.get_odes()
        # rM = {'A': [['-18', 'A', 'B'], ['-99', 'A']], 'C': [['18', 'A', 'B'], ['99', 'A']], 'B': [['-18', 'A', 'B']], 'E': [['99', 'A']]}
        # rR = {}
        # self.assertItemsEqual(M, rM)
        # self.assertDictEqual(R, rR)

        # M, R = RG.get_odes(rate_dict=True)
        # rM = {'A': [['-k0', 'A', 'B'], ['-k1', 'A']], 'C': [['k0', 'A', 'B'], ['k1', 'A']], 'B': [['-k0', 'A', 'B']], 'E': [['k1', 'A']]}
        # rR = {'k1': 99, 'k0': 18}
        # self.assertDictEqual(M, rM)
        # self.assertDictEqual(R, rR)


if __name__ == '__main__':
    unittest.main()
