from dataclasses import dataclass
from reactions import Reactions
from species import Species

from functools import singledispatch

from configuration import DtypeKey,DtypeIndex,DtypeCount,DtypeCoefficient

Key = DtypeKey
Index = DtypeIndex

@dataclass(frozen=True)
class Index:
    species_index: Dict[Key,Index]
    reactions_index: Dict[Key,Index]

def index_factory(reactions: Reactions) -> Index:
    species_index = assign_species_index(reactions)
    reactions_index = assign_reactions_index(reactions)

    return Index(species_index,reactions_index)

@singledispatch
def assign_species_index(obj: Species | Reactions) -> Dict[Key,Index]:
    raise TypeError(f"{obj} is not of type Species | Reactions")

@assign_species_index.register
def _(species: Species) -> Dict[Key,Index]:
    pass

@assign_species_index.register
def _(reactions: Reactions) -> Dict[Key,Index]:
    pass

def assign_reactions_index(reactions: Reactions) -> Dict[Key,Index]:
    if not isinstance(reactions,Reactions):
        raise TypeError(f"{reactions} is not of type Reactions")
    pass