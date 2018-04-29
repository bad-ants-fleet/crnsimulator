#
# CRN-to-MultiDiGraph-to-ODE translation utilities.
#
# Written by Stefan Badelt (badelt@caltech.edu).
#
# Use at your own risk.
#
#

from builtins import zip
from builtins import str
from builtins import map
from builtins import range
from builtins import object
import networkx as nx
from sympy import sympify, Matrix, Symbol

from crnsimulator.solver import writeODElib


class CRNSimulatorError(Exception):
    def __init__(self, message):
        super(CRNSimulatorError, self).__init__(message)


class ReactionNode(object):
    """A Reaction-Node in the ReactionGraph class. """
    rid = 0

    def __init__(self, prefix='RXN:'):
        self._name = prefix + str(ReactionNode.rid)
        ReactionNode.rid += 1

    @property
    def name(self):
        return self._name


class ReactionGraph(object):
    """Basic Reaction Graph Object. """

    def __init__(self, crn=None, nxgraph=None):
        self._RG = nx.MultiDiGraph()
        if crn:
            self.add_reactions(crn)
        elif nxgraph:
            raise CRNSimulatorError(
                'Initialization from Graph is not implemented.')
            self._RG = nx.MultiDiGraph(nxgraph)
            self._rnode = lambda g_n: g_n[0].g_n[1]
            self._rates = lambda g_n1: g_n1[0].g_n1[1]
            self._exclude = lambda g_n2: g_n2[0].g_n2[1]
            self._rename = None

    #@property
    # def reactions(self):
    #  return [n for n in self._RG.nodes() if isinstance(n, ReactionNode)]

    @property
    def species(self):
        return [n for n in self._RG.nodes() if not isinstance(n, ReactionNode)]

    @property
    def reactants(self):
        return [n for n in self._RG.nodes() if not isinstance(n, ReactionNode)
                and self._RG.out_edges(n)]

    @property
    def products(self):
        return [n for n in self._RG.nodes() if not isinstance(n, ReactionNode)
                and self._RG.in_edges(n)]

    def write_ODE_lib(self, sorted_vars=None, concvect=None, jacobian=False, rate_dict=False,
                      odename='odesystem', filename='./odesystem', template=None):

        if concvect:
            assert len(concvect) == len(sorted_vars)

        V, M, J, R = self.ode_system(
            sorted_vars=sorted_vars, jacobian=jacobian, rate_dict=rate_dict)

        return writeODElib(V, M, jacobian=J, rdict=R, concvect=concvect,
                           odename=odename, filename=filename, template=None)

    def ode_system(self, sorted_vars=None, jacobian=False, rate_dict=False):
        odict, rdict = self.get_odes(rate_dict=rate_dict)

        if sorted_vars:
            sorted_vars = list(map(Symbol, sorted_vars))
            assert len(sorted_vars) == len(list(odict.keys()))
        else:
            sorted_vars = sorted(list(odict.keys()), key=lambda x: str(x))

        # Symbol namespace dictionary, translates every variable name into a Symbol,
        #   even awkward names such as 'sin' or 'cos'
        ns = dict(zip(map(str, sorted_vars), sorted_vars))

        M = []
        for dx in sorted_vars:
            sfunc = sympify(
                ' + '.join(['*'.join(map(str, xp)) for xp in odict[dx]]), locals=ns)
            odict[dx] = sfunc
            M.append(sfunc)
        M = Matrix(M)

        if jacobian:
            # NOTE: The sympy version breaks regularly:
            # J = M.jacobian(sorted_vars)
            # ... so it is done per pedes:
            J = []
            for f in M:
                for x in sorted_vars:
                    J.append(f.diff(x))
            J = Matrix(J)
        else:
            J = None

        return sorted_vars, M, J, rdict

    def get_odes(self, rate_dict=False):
        """Translate the reaction graph into ODEs.

        Returns:
          sympy.Symbols

        """
        rdict = dict()
        odes = dict()
        for rxn in self._RG.nodes():
            if not isinstance(rxn, ReactionNode):
                continue
            if rate_dict:
                rate = 'k' + str(len(list(rdict.keys())))
                rdict[rate] = self._RG.node[rxn]['rate']
            else:
                rate = str(self._RG.node[rxn]['rate'])

            reactants = []
            for reac in self._RG.predecessors(rxn):
                for i in range(self._RG.number_of_edges(reac, rxn)):
                    reactants.append(Symbol(reac))

            products = []
            for prod in self._RG.successors(rxn):
                for i in range(self._RG.number_of_edges(rxn, prod)):
                    products.append(Symbol(prod))

            for x in reactants:
                if x in odes:
                    odes[x].append(['-' + rate] + reactants)
                else:
                    odes[x] = [['-' + rate] + reactants]

            for x in products:
                if x in odes:
                    odes[x].append([rate] + reactants)
                else:
                    odes[x] = [[rate] + reactants]

        return odes, rdict

    def add_reactions(self, crn):
        assert isinstance(crn, list)
        for rxn in crn:
            self.add_reaction(rxn)
        return

    def add_reaction(self, rxn):
        assert len(rxn) == 3
        n = ReactionNode()
        # sometimes the format is [[react],[prod], [k]],
        # sometimes it is [[react],[prod], k]
        rxn[2] = rxn[2] if not isinstance(rxn[2], list) else rxn[2][0]
        self._RG.add_node(n, rate=rxn[2])
        for r in rxn[0]:
            # breaks with utf-8 strings... unfortunately
            #assert isinstance(r, str)
            self._RG.add_edge(r, n)
        for p in rxn[1]:
            #assert isinstance(p, str)
            self._RG.add_edge(n, p)
        return
