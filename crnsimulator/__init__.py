##############################################
# Initiation of the nuskell compiler package #
##############################################

__version__ = "0.0.1"

# Import the compiler I/O base #
from crnsimulator.solver import main, writeODElib
from crnsimulator.reactiongraph import crn_to_ode, CRN_to_MultiDiGraph, MultiDiGraph_to_ODE
