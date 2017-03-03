#
# Deprecated interface: A collection of CRNs.
# 
# Written by Stefan Badelt (badelt@caltech.edu).
#
# Use at your own risk. 
#
#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 

def oscillator(fw1=0.2, fw2=0.3, fw3=0.7):
  return [[['A', 'B'], ['B', 'B'], fw1],
          [['B', 'C'], ['C', 'C'], fw2],
          [['C', 'A'], ['A', 'A'], fw3]] 

def roessler(fw1=30, fw2=0.5, fw3=1, fw4=10, fw5=1, fw6 =16.5, fw7=0.5):
  """ SoSeWi
  X1 -> 2X1 [fw=30]
  2X1 -> X1 [fw=0.5]
  X2 + X1 -> 2X2
  X2 -> 
  X1 + X3 ->
  X3 -> 2X3
  2X3 -> X3
  """
  return [[['X1'],['X1', 'X1'],fw1],
          [['X1', 'X1'],['X1'],fw2],
          [['X2', 'X1'],['X2', 'X2'], fw3],
          [['X2'],[],fw4],
          [['X1', 'X3'],[],fw5],
          [['X3'],['X3', 'X3'],fw6],
          [['X3', 'X3'],['X3'],fw7]]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 

def binary_counter(fw1=0.5, bw1=0.1, fw2=0.5, bw2=1, fw3=0.5, bw3=0.1):
  """ A binary counter with three digits:
  # taken from: 

  On : The nth bit is 0
  In : The nth bit is 1

  O1 <=> I1
  O2 + I1 <=> I2 + O1
  O3 + I2 + I1 <=> I3 + O2 + O1
  """
  return [[['O1'], ['I1'], fw1],
          [['I1'], ['O1'], bw1],
          [['O2', 'I1'], ['I2', 'O1'], fw2],
          [['I2', 'O1'], ['O2', 'I1'], bw2],
          [['O3', 'I2', 'I1'], ['I3', 'O2', 'O1'], fw3],
          [['I3', 'O2', 'O1'], ['O3', 'I2', 'I1'], bw3]]

def catalyst(fw1=0.2):
  return [[['A', 'B'], ['A', 'A'], fw1]]

def templated_autocatalysis(fw1=0.2):
  return [[['A', 'B', 'C'], ['C', 'C'], fw1]]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 
def a_gt_b(fw1=1, fw2=1):
  """ Predicate: #A > #B

  Start with 1 F and input amounts of A, B
  
  T : True
  F : False
  """
  return [[['A', 'F'],['T'],fw1],
          [['B', 'T'],['F'],fw2]]

def a_even(fw1=1, fw2=1):
  """ Predicate: #A is even

  Start with 1 T and input amount of A
  """
  return [[['A', 'T'],['F'],fw1],
          [['A', 'F'],['T'],fw2]]

def a_gt_b_and_a_even(fw1=1, fw2=1):
  """ Predicate: #A > #B and #A is even

  Start with 1 FI, 1 T2, 1 F and iput amounts of A, B
  """
  pass

def oregonator():
  """ DNA as a universal substrate for chemical kinetics
  X2 -> X1 
  X1+X2 ->
  X1 -> 2X1 + X3
  2X1 -> 
  X3 -> X2
  X3 ->
  """
  pass

def two_bit_pulse_counter():
  pass

def incrementor_state_machine():
  pass

def majority():
  """
  X + Y -> 2B
  X + B -> 2X
  Y + B -> 2Y
  """

def devide_and_conquer():
  """
  A -> 2A
  2A -> B + B
  B -> A
  """

def mypredprey():
  """ 
  Food source gets produce spontanously, 

  -> F [fw=1]
  F + A -> A + A [fw=10]
  A + B -> B + B [fw=8]
  B -> [fw = 0.5]
  A -> [fw = 0.5]
  """

def fibonacci():
  """
  Y -> O 
  O -> Y + O
  """

def predator_prey():
  """

  X1 + X2 -> X2 + X2
  X1 -> X1 + X1
  X2 -> 

  k1 = 1.5 or 5*10^5 /M/s
  k2 = 1   or 1/300 /s
  k3 = 1   or 1/300 /s

  """


