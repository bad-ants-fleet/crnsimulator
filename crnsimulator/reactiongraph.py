#
# CRN-to-MultiDiGraph-to-ODE translation utilities.
#
# Written by Stefan Badelt (badelt@caltech.edu).
#
# Use at your own risk.
#
#

import networkx as nx
from typing import Dict, List, Tuple, Sequence, TypeVar, Union
from sympy import sympify, Matrix, Symbol

from crnsimulator.solver import writeODElib

# Typehintsh
SPE = List[str]
RXN = Tuple[SPE, SPE, str]
CRN = List[RXN]
sM = TypeVar('sympy.Matrix')


class CRNSimulatorError(Exception):
    def __init__(self, message):
        super(CRNSimulatorError, self).__init__(message)


class ReactionNode(object):
    """A Reaction-Node in the ReactionGraph class. """
    rid = 0
    def __init__(self, prefix: str = 'RXN:'):
        self.name = prefix + str(ReactionNode.rid)
        ReactionNode.rid += 1

class ReactionGraph(object):
    """Basic Reaction Graph Object. """

    def __init__(self, crn: CRN = None):
        self._RG = nx.MultiDiGraph()
        if crn: self.add_reactions(crn)

    @property
    def reactions(self):
        return [n for n in self._RG.nodes() if isinstance(n, ReactionNode)]

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

    def write_ODE_lib(self, 
            sorted_vars: List[str] = None, 
            concvect: List[float] = None, 
            jacobian: bool = False, 
            rate_dict: bool = False,
            odename: str = 'odesystem', 
            filename: str = './odesystem', 
            template: str = None):
        """
        Produce ODE system, load a template file and write an executable python script.
        """

        if concvect and len(concvect) != len(sorted_vars):
            raise CRNSimulatorError('Concentrations cannot be mapped to species!')

        V, M, J, R = self.ode_system(sorted_vars = sorted_vars, 
                                     jacobian = jacobian, 
                                     rate_dict = rate_dict)

        return writeODElib(V, M, jacobian = J, rdict = R, concvect = concvect,
                           odename = odename, filename = filename, template = None)

    def ode_system(self, 
            sorted_vars: List[str] = None, 
            jacobian: bool = False, 
            rate_dict: bool = False) -> Tuple[List[str], 
                                              sM, 
                                              Union[sM, None], 
                                              Union[Dict[str, str], None]]:

        odict, R = self.get_odes(rate_dict = rate_dict)

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

        return sorted_vars, M, J, R 

    def get_odes(self, rate_dict: bool = False) -> Tuple[
            Dict[str, List[str]], Union[Dict[str, str], None]]:
        """Translate the reaction graph into ODEs.
        """
        rdict = dict()
        odes = dict()

        for rxn in self.reactions:
            if rate_dict:
                rate = 'k' + str(len(list(rdict.keys())))
                rdict[rate] = self._RG.nodes[rxn]['rate']
            else:
                rate = str(self._RG.nodes[rxn]['rate'])

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

    def add_reactions(self, crn: CRN) -> None:
        assert isinstance(crn, list)
        for rxn in crn:
            self.add_reaction(rxn)

    def add_reaction(self, rxn: RXN) -> None:
        assert len(rxn) == 3
        n = ReactionNode()

        if isinstance(rxn[2], list):
            # TODO: for now it is ok, but maybe we should enforce a consistent format here.
            #
            # sometimes the format is [[react],[prod], [k]],
            # sometimes it is [[react],[prod], k]
            #
            # print(DeprecationWarning('Using deprecated format for irreversible reactions.'))
            rxn[2] = rxn[2][0]

        self._RG.add_node(n, rate = rxn[2])
        for r in rxn[0]:
            assert isinstance(r, str)
            self._RG.add_edge(r, n)
        for p in rxn[1]:
            assert isinstance(p, str)
            self._RG.add_edge(n, p)

        return
