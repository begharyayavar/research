from typing import Dict
from manager import Key,Count
from species import Species

from dataclasses import dataclass

from manager import Name,Index

@dataclass
class InitialConditions:
    specie_counts: Dict[Key,Count]

def get_specie_counts_by_name(species: Species,initial_conditions: InitialConditions) -> Dict[SpecieName,Count]:
    return {specie.name:initial_conditions.specie_counts[specie.key] \
                for specie in species.species}

def get_specie_counts_by_index(species: Species,initial_conditions: InitialConditions) -> Dict[SpecieIndex,Count]:
    return {species.specie_index[specie.key]:initial_conditions.specie_counts[specie.key] \
                for specie in species.species}