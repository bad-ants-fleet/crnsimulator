
def oscillator(fw1=0.2, fw2=0.3, fw3=0.7):
  return [[['A', 'B'], ['A', 'A'], fw1],
          [['B', 'C'], ['B', 'B'], fw2],
          [['C', 'A'], ['C', 'C'], fw3]] 

def catalyst(fw1=0.2):
  return [[['A', 'B'], ['A', 'A'], fw1]]

def bin_counter(fw1=0.5, bw1=0.1, fw2=0.5, bw2=1, fw3=0.5, bw3=0.1):
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

def roessler():
  """ SoSeWi
  X1 -> 2X1
  2X1 -> X1
  X2 + X1 -> 2X2
  X2 -> 
  X1 + X3 ->
  X3 -> 2X3
  2X3 -> X3
  """
  pass

