import networkx as nx
from sympy import sympify

def crn_to_ode(crn, rate_dict = True, symplification = True):
  """A wrapper function for CRN_to_MultiDigraph() and MultiDigraph_to_ODE(). """
  crn2, ode, rdict = MultiDiGraph_to_ODE(CRN_to_MultiDiGraph(crn), rate_dict = rate_dict)

  crn = sorted(map(lambda x: [sorted(x[0]), sorted(x[1]), x[2]], crn))
  crn2 = sorted(map(lambda x: [sorted(x[0]), sorted(x[1]), x[2]], crn2))
  assert crn == crn2

  for dx in ode.keys():
    sfunc = sympify(' + '.join(['*'.join(map(str,xp)) for xp in ode[dx]]))
    ode[dx] = sfunc

  if rate_dict :
    return ode, rdict
  else :
    return ode

def CRN_to_MultiDiGraph(crn):
  """ """
  RG = nx.MultiDiGraph()
  num = 0
  for reaction in crn :
    hyper= 'REACT:' + str(num)
    rate = reaction[2]
    for reac in reaction[0]:
      RG.add_weighted_edges_from([(reac, hyper, rate)])
    for prod in reaction[1]:
      RG.add_weighted_edges_from([(hyper, prod, rate)])
    RG.node[hyper]['rate'] = rate
    num += 1
  return RG

def MultiDiGraph_to_ODE(RG, rate_dict = False):
  """ Translate a networkx MultiDiGraph into a ODE system.
  
  For every reaction vertex, append the respective species to a dictionary of
  nodes. Every species is a node in the graph, so the information of which
  species is consumed and produced can simply be appended to 

  ndict['A'] = ['k1','A','B'] + ['-k2', 'B', 'C']

  ... where k1 is a string that contains either the actual number, or the key for 
  a separate rate_dictionary. The latter is usefull when solving ODEs with 
  scipy.odeint(). Otherwise simulations are extremely unstable.

  Returns:
    crn (list([k1, [A,B], [A,A]]))
    ndict (ndict['A'] = [['k1','A','B'], ['-k2', 'B', 'C']])
    rdict (rdict['k1'] = 0.2)
  
  """
  ndict = {}
  rdict = {}
  crn = []
  ode = {}
  for r in RG.nodes_iter() :
    if r[:6] != 'REACT:' : continue
    if rate_dict :
      rate = 'k'+str(len(rdict.keys()))
      rdict[rate] = RG.node[r]['rate']
      #rate = 'r['+rate+']'
    else :
      rate = str(RG.node[r]['rate'])

    reactants = []
    for reac in RG.predecessors_iter(r) :
      for i in range(RG.number_of_edges(reac, r)) :
        reactants.append(reac)

    products = []
    for prod in RG.successors_iter(r) :
      for i in range(RG.number_of_edges(r, prod)) :
        products.append(prod)
 

    for x in reactants: 
      if x in ode :
        ode[x].append(['-'+rate] + reactants)
      else :
        ode[x]= [['-'+rate] + reactants]

    for x in products: 
      if x in ode :
        ode[x].append([rate] + reactants)
      else :
        ode[x]= [[rate] + reactants]

    crn.append([reactants, products, RG.node[r]['rate']])
  return crn, ode, rdict

