#
# Unittests for crnsimulator.crn_parser
#
# Written by Stefan Badelt (badelt@caltech.edu).
#

import unittest
from pyparsing import ParseException
from crnsimulator.crn_parser import parse_crn_string

class TestCRNparser(unittest.TestCase):

    def test_concentration_specs(self):
        input_string = """
        # Default concentrations
        A @ initial 50
        B @ constant 50
        C @ constant 10

        # Reactions
        A + B -> C
        """
        output_unprocessed = [['concentration', ['A'], ['initial'], ['50']],
                              ['concentration', ['B'], ['constant'], ['50']],
                              ['concentration', ['C'], ['constant'], ['10']],
                              ['irreversible', [['A'], ['B']], [['C']]]]

        self.assertEqual(parse_crn_string(input_string, process=False), output_unprocessed)

        output_processed1 = [[['A', 'B'], ['C'], [1]]]
        output_processed2 = {'A' : ('initial', 50),
                             'B' : ('constant', 50),
                             'C' : ('constant', 10)}

        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)
        self.assertEqual(o2, output_processed2)
 
        input_string = "A@i50; B@c20; A + B -> C [k = 77]; <=> C [kf = 18, kr = 77]"
        output_unprocessed = [['concentration', ['A'], ['i'], ['50']],
                              ['concentration', ['B'], ['c'], ['20']],
                              ['irreversible', [['A'], ['B']], [['C']], ['77']],
                              ['reversible', [], [['C']], ['18', '77']] ]

        self.assertEqual(parse_crn_string(input_string, process=False), output_unprocessed)

        output_processed1 = [[['A', 'B'], ['C'], ['77']],
                             [[],['C'],['18', '77']]]
        output_processed2 = {'A' : ('initial', 50),
                             'B' : ('constant', 20),
                             'C' : ('initial', 0)}

        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)
        self.assertEqual(o2, output_processed2)

    def test_float_examples(self):
        input_string = """
        # Comment
        A + B -> C [k = 0.32]
        """
        output_unprocessed = [['irreversible', [['A'], ['B']], [['C']]]]
        output_processed1 = [[['A', 'B'], ['C'], ['0.32']]]
        output_processed2 = {'A' : ('initial', 0),
                             'B' : ('initial', 0),
                             'C' : ('initial', 0)}
        # print parse_crn_string(input_string, process=False)
        # print parse_crn_string(input_string)
 
    def test_parse_examples(self):
        input_string = """
        # Comment
        A + B -> C
        """
        output_unprocessed = [['irreversible', [['A'], ['B']], [['C']]]]
        output_processed1 = [[['A', 'B'], ['C'], [1]]]
        output_processed2 = {'A' : ('initial', 0),
                             'B' : ('initial', 0),
                             'C' : ('initial', 0)}
        output_processed3 = [[['A', 'B'], ['C'], [1]]]
        output_processed4 = {'A' : (None, None),
                             'B' : (None, None),
                             'C' : (None, None)}
        # print parse_crn_string(input_string, process=False)
        # print parse_crn_string(input_string)
        self.assertEqual(parse_crn_string(input_string, process=False), 
                         output_unprocessed,
                         'parse reaction unprocessed 1')
        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)
        self.assertEqual(o2, output_processed2)

        o3, o4 = parse_crn_string(input_string, process = True, defaultrate = 1, defaultmode = None, defaultconc = None)
        self.assertEqual(o3, output_processed3)
        self.assertEqual(o4, output_processed4)

        input_string = """A + B -> C [k = 10.8]"""
        output_unprocessed = [['irreversible', [['A'], ['B']], [['C']], ['10.8']]]
        output_processed1 = [[['A', 'B'], ['C'], ['10.8']]]
        self.assertEqual(parse_crn_string(input_string, process=False),
                         output_unprocessed,
                         'parse reaction unprocessed 2')
        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)
        self.assertEqual(o2, output_processed2)

        input_string = """A + B -> C [k = 8]"""
        output_unprocessed = [['irreversible', [['A'], ['B']], [['C']], ['8']]]
        output_processed1 = [[['A', 'B'], ['C'], ['8']]]
        self.assertEqual(parse_crn_string(input_string, process=False),
                         output_unprocessed,
                         'parse reaction unprocessed 3')
        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)
        self.assertEqual(o2, output_processed2)

        with self.assertRaises(ParseException):
            # Only one rate specified for reversible reaction
            parse_crn_string("A <=> C [k=14]")

    def test_duplicate_input(self):
        input_string = """ # Allowing duplicate specification!
        A + B -> C
        A + B <=> C
        """
        output_unprocessed = [['irreversible', [['A'], ['B']], [['C']]], 
                              ['reversible', [['A'], ['B']], [['C']]]]
        output_processed1 = [[['A', 'B'], ['C'], [1]], 
                            [['A', 'B'], ['C'], [1, 1]]]
        output_processed2 = {'A' : ('initial', 0),
                             'B' : ('initial', 0),
                             'C' : ('initial', 0)}
        self.assertEqual(parse_crn_string(input_string, process=False),
                         output_unprocessed,
                         'parse reaction unprocessed 4')
        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)
        self.assertEqual(o2, output_processed2)

        input_string = """
        # Comment
        A + B -> C [k = 18]
        A + B <=> C [kf = 99, kr = 77]
        """
        output_unprocessed = [['irreversible', [['A'], ['B']], [['C']], ['18']], 
                              ['reversible', [['A'], ['B']], [['C']], ['99', '77']]]
        output_processed1 = [[['A', 'B'], ['C'], ['18']], 
                            [['A', 'B'], ['C'], ['99', '77']]]
        self.assertEqual(parse_crn_string(input_string, process=False),
                         output_unprocessed,
                         'parse reaction unprocessed 5')
        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)

        input_string = """
        # Comment
        A + B -> C [18]
        A + B <=> C [99, 77]
        """
        output_unprocessed = [['irreversible', [['A'], ['B']], [['C']], ['18']], 
                              ['reversible', [['A'], ['B']], [['C']], ['99', '77']]]
        output_processed1 = [[['A', 'B'], ['C'], ['18']], 
                            [['A', 'B'], ['C'], ['99', '77']]]
        self.assertEqual(parse_crn_string(input_string, process=False),
                         output_unprocessed,
                         'parse reaction unprocessed 5')
        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)

        input_string = "A + B -> C + X [0.48]; X + A <=> C + L [0.89, 0.87]"
        exp1 = [[['A', 'B'], ['C', 'X'], ['0.48']], [['X', 'A'], ['C', 'L'], ['0.89', '0.87']]]
        exp2 = {'A': ('initial', 0), 'B': ('initial', 0), 'C': ('initial', 0), 'X': ('initial', 0), 'L': ('initial', 0)}

        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, exp1)


    def test_multiple_species(self):
        input_string = """5A -> 3B + 2C"""
        output_processed1 = [[['A', 'A', 'A', 'A', 'A'], 
                             ['B', 'B', 'B', 'C', 'C'], [1]]]
        output_processed2 = {'A' : ('initial', 0),
                             'B' : ('initial', 0),
                             'C' : ('initial', 0)}
        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)
        self.assertEqual(o2, output_processed2)

        input_string = """
        A + B -> C [k = 77]; <=> C [kf = 18, kr = 77]
        X + 2Y <=> Z
        """
        output_processed1 = [[['A', 'B'], ['C'], ['77']], [[], ['C'], ['18', '77']], 
                            [['X', 'Y', 'Y'], ['Z'], [1, 1]]]
        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)

        input_string = """2Na + Cl2 <=> 2NaCl"""
        output_processed1 = [[['Na', 'Na', 'Cl2'], ['NaCl', 'NaCl'], [1, 1]]]
        output_processed2 = {'Na' : ('initial', 0),
                             'Cl2' : ('initial', 0),
                             'NaCl' : ('initial', 0)}
        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)
        self.assertEqual(o2, output_processed2)

        input_string = """N2 + 3H2 <=> 2NH3"""
        output_processed1 = [[['N2', 'H2', 'H2', 'H2'], ['NH3', 'NH3'], [1, 1]]]
        output_processed2 = {'N2' : ('initial', 0),
                             'H2' : ('initial', 0),
                             'NH3' : ('initial', 0)}
        o1, o2 = parse_crn_string(input_string)
        self.assertEqual(o1, output_processed1)
        self.assertEqual(o2, output_processed2)


if __name__ == '__main__':
    unittest.main()
