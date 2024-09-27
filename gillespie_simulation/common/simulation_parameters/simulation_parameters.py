import numpy as np
import numpy.typing as npt
from typing import List,Self,Dict,Set,Iterable
from dataclasses import dataclass
from itertools import chain
from utils import is_string_filename,is_string_reaction,is_string_initial_condition
from common.manager import SpecieKey,SpecieIndex,SpecieName,ReactionKey,ReactionIndex

from reactions import Reactions

from configuration import DtypeCount,DtypeCoefficient

Coefficient = DtypeCoefficient
Count = DtypeCount



@dataclass
class ComputeParameters:
    num_steps: DTypeCSA
    num_cycles:  DTypeCSA
    num_averages: DTypeCSA

    num_species: np.uint8
    reactant_indices: np.ndarray
    reactant_coeficients: np.ndarray

    rate_constants: np.ndarray
    reaction_matrix: np.ndarray

    initial_conditions: np.ndarray

@dataclass
class SimulationParameters:
    _num_cycles: DTypeCSA = DEFAULT_NUM_CYCLES
    _num_steps: DTypeCSA = DEFAULT_NUM_STEPS
    _num_averages: DTypeCSA = DEFAULT_NUM_STEPS

    _reactions: Reactions = Reactions()
    _index: Index = Index()

def convert(simulationparameters: SimulationParameters) -> ComputeParameters:

    num_cycles = simulationparameters.num_cycles
    num_steps = simulationparameters.num_steps
    num_averages = simulationparameters.num_averages

    num_species = len(simulationparameters.reactions.species)

    reactant_indices = calculate_reactant_indices(simulationparameters.reactions)
    reactant_coeficients = calculate_reactant_coefficients(simulationparameters.reactions)

    reaction_matrix =  calculate_reaction_matrix(simulationparameters.reactions)
    rate_constants=  calculate_rate_constants(simulationparameters.reactions)

    initial_conditions =  calculate_initial_conditions(simulationparameters.reactions)

def calculate_reactant_indices(reactions: Reactions):
    pass

def calculate_reactant_coefficients(reactions: Reactions):
    pass

def calculate_reaction_matrix(reactions: Reactions):
    pass

def calculate_rate_constants(reactions: Reactions):
    pass

def calculate_initial_conditions(reactions: Reactions):
    pass

