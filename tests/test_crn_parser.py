import unittest
from pyparsing import ParseException
from crnsimulator.crn_parser import parse_crn_string

class TestCRNparser(unittest.TestCase):
  #def setUp(self):
  #  pass

  #def tearDown(self):
  #  pass

  def test_parse_examples(self):
    input_string = """
    # Comment
    A + B -> C
    """
    output_unprocessed = [['irreversible',[['A'],['B']],[['C']]]]
    output_processed = [[['A','B'], ['C'], [None]]], set(['A','B','C'])
    #print parse_crn_string(input_string, process=False)
    #print parse_crn_string(input_string)
    self.assertEqual(parse_crn_string(input_string, process=False), output_unprocessed, 'parse reaction unprocessed 1')
    self.assertEqual(parse_crn_string(input_string), output_processed, 'parse reaction processed 1')

    input_string = """
    A + B -> C [k = 10.8]
    """
    output_unprocessed = [['irreversible',[['A'],['B']],[['C']], ['10.8']]]
    output_processed = [[['A','B'],['C'], ['10.8']]], set(['A','B','C'])
    #print parse_crn_string(input_string, process=False)
    #print parse_crn_string(input_string)
    self.assertEqual(parse_crn_string(input_string, process=False), output_unprocessed, 'parse reaction unprocessed 2')
    self.assertEqual(parse_crn_string(input_string), output_processed, 'parse reaction processed 2')

    input_string = """
    A + B -> C [k = 8]
    """
    output_unprocessed = [['irreversible',[['A'],['B']],[['C']], ['8']]]
    output_processed = [[['A','B'],['C'], ['8']]], set(['A','B','C'])
    #print parse_crn_string(input_string, process=False)
    #print parse_crn_string(input_string)
    self.assertEqual(parse_crn_string(input_string, process=False), output_unprocessed, 'parse reaction unprocessed 3')
    self.assertEqual(parse_crn_string(input_string), output_processed, 'parse reaction processed 3')

    input_string = """ # Allowing duplicate specification!
    A + B -> C
    A + B <=> C
    """
    output_unprocessed = [['irreversible',[['A'],['B']],[['C']]], ['reversible',[['A'],['B']],[['C']]]]
    output_processed = [[['A','B'],['C'], [None]], [['A','B'],['C'],[None,None]]], set(['A','B','C'])
    #print parse_crn_string(input_string, process=False)
    #print parse_crn_string(input_string)
    self.assertEqual(parse_crn_string(input_string, process=False), output_unprocessed, 'parse reaction unprocessed 4')
    self.assertEqual(parse_crn_string(input_string), output_processed, 'parse reaction processed 4')

    input_string = """
    # Comment
    A + B -> C [k = 18]
    A + B <=> C [kf = 99, kr = 77]
    """
    output_unprocessed = [['irreversible',[['A'],['B']],[['C']], ['18']], ['reversible',[['A'],['B']],[['C']], ['99','77']]]
    output_processed = [[['A','B'],['C'], ['18']], [['A','B'],['C'], ['99','77']]], set(['A','B','C'])
    #print parse_crn_string(input_string, process=False)
    #print parse_crn_string(input_string)
    self.assertEqual(parse_crn_string(input_string, process=False), output_unprocessed, 'parse reaction unprocessed 5')
    self.assertEqual(parse_crn_string(input_string), output_processed, 'parse reaction processed 5')

    input_string = """5A -> 3B + 2C"""
    output_processed = [[['A', 'A', 'A', 'A', 'A'],['B','B','B','C','C'],[None]]], set(['A','B','C'])
    #print parse_crn_string(input_string)
    self.assertEqual(parse_crn_string(input_string), output_processed, 'parse reaction processed 6')

    input_string = """
    A + B -> C [k = 77]; <=> C [kf = 18, kr = 77]
    X + 2Y <=> Z
    """
    output_processed = [[['A', 'B'], ['C'], ['77']], [[], ['C'], ['18', '77']], [['X', 'Y', 'Y'], ['Z'], [None, None]]], set(['A','B','C','X','Y','Z'])
    #print parse_crn_string(input_string)
    self.assertEqual(parse_crn_string(input_string), output_processed, 'parse reaction processed 7')

    input_string = """2Na + Cl2 <=> 2NaCl"""
    #print parse_crn_string(input_string)
    output_processed = [[['Na', 'Na', 'Cl2'], ['NaCl', 'NaCl'], [None, None]]], set(['Na', 'Cl2', 'NaCl'])
    self.assertEqual(parse_crn_string(input_string), output_processed, 'parse reaction processed 8')

    input_string = """N2 + 3H2 <=> 2NH3"""
    #print parse_crn_string(input_string)
    output_processed = [[['N2', 'H2', 'H2', 'H2'], ['NH3', 'NH3'], [None, None]]], set(['N2', 'H2', 'NH3'])
    self.assertEqual(parse_crn_string(input_string), output_processed, 'parse reaction processed 9')
 
    with self.assertRaises(ParseException):
      # Only one rate specified for reversible reaction
      parse_crn_string("A <=> C [k=14]")

if __name__ == '__main__':
  unittest.main()

