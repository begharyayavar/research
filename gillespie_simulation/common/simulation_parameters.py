import numpy as np
from typing import List,Self,Dict,Set
from dataclasses import dataclass

from utils import is_string_filename,is_string_reaction,is_string_initial_condition

type Key = int
type Index = np.uint8
type SpecieName = str
type Count = np.uint8
type Coefficients = np.uint8

@dataclass
class Specie:
    key: Key
    name: SpecieName

@dataclass
class Species:
    specie_index: Dict[Key,Index]
    species: Set[Specie]

@dataclass
class Reaction:
    key: Key
    reactants: Species
    products: Species
    Rf: np.floating
    coefficients: Coefficients
    reactant_indices: List[Index]
    product_indices: List[Index]

@dataclass
class Reactions:
    reaction_index: Dict[Key,Index]
    reactions: Set[Reaction]

@dataclass
class InitialConditions:
    specie_counts: Dict[Key,Count]

def get_specie_counts_by_name(species: Species,initial_conditions: InitialConditions) -> Dict[SpecieName,Count]:
    return {specie.name:initial_conditions.specie_counts[specie.key] \
                for specie in species.species}

def get_specie_counts_by_index(species: Species,initial_conditions: InitialConditions) -> Dict[Index,Count]:
    return {species.specie_index[specie.key]:initial_conditions.specie_counts[specie.key] \
                for specie in species.species}

class SimulationParameters:
    def __init__(self: Self):
        # self.species = Species()
        # self.reaction = Reactions()
        # self.initial_specie_counts = InitialConditions()
        # self.reactant_indices = None
        # self.rate_constants = None
        pass

    def add(self: Self,string: str):
        if is_string_filename(string):
            species,\
            reactions,\
            reactant_indices,\
            rate_constants,\
            initial_specie_counts = reaction_parser(string)

        if is_string_reaction(string):
            pass

        if is_string_initial_condition(string):
            pass


def calculate_reaction_matrix(species: List[Specie],reactions: List[Reaction]):


