import sys
sys.path.append('../../common')

from typing import Iterable,Dict,Self,List
from itertools import chain
import numpy as np
from species import Specie,specie_factory,Species,species_factory
from initial_conditions import InitialConditions
from dataclasses import dataclass
from reaction_parser import parse_reactants,parse_products,parse_coefficients,parse_Rf
from utils import is_string_reaction
from functools import singledispatch

@dataclass(frozen=True)
class Reaction:

    key: int
    name: str

    reactants: Species
    products: Species
    rf: float
    coefficients: Dict[Specie,Coefficient]

    def __add__(self: "Reaction",reaction: "Reaction") -> "Reaction":
        pass


    def __repr__(self: "Reaction") -> str:
        return f"\n{self.name} \tkey = {self.key}\n"

def reaction_factory(obj: str | Reaction) -> Reaction:
    if isinstance(obj,Reaction):
        return obj
    if isinstance(obj,str):
        if is_string_reaction(obj):
            key: int = generate_key_reaction(obj)
            name: str = generate_name_reaction(obj)
            reactants: Species = species_factory(parse_reactants(obj))
            products: Species = species_factory(parse_products(obj))
            rf: float = parse_Rf(obj)
            coefficients: Dict[Specie,Coefficient] = {specie_factory(specie): Coefficient(coefficient) \
                                for specie,coefficient in parse_coefficients(obj)}

            return Reaction(key,name,reactants,products,rf,coefficients)

        else:
            raise ValueError(f"{obj} is not a valid Reaction. Please check documentation for syntax")
    raise ValueError(f"{obj} is invalid as an instatiantor of Reaction. It must be of type str | Reaction")


class Reactions:
    def __init__(self,reactions: Iterable[Reaction]):

        self.reactions = reactions

        self._species : Species
        self._initial_conditions : InitialConditions


    @property
    def reactions(self):
        return self._reactions

    @reactions.setter
    def reactions(self,value: Iterable[Reaction]):
        self._reactions = list(value)
        self.refresh_initial_conditions()

    @property
    def species(self):
        return species_factory({specie for reaction in self.reactions for specie in reaction.reactants + reaction.products})

    @property
    def initial_conditions(self):
        return self._initial_conditions


    @property
    def keys(self):
        return [reaction.key for reaction in self.reactions]

    def add_reaction(self,obj: str | Reaction) -> Self:
        if generate_key_reaction(obj) not in self.keys:
            self.reactions = list(chain(self.reactions,[reaction_factory(obj)]))
        return self


    def remove_reaction(self,key: ReactionKey) -> Self:
        self.reactions = [reaction for reaction in self.reactions if reaction.key != key]
        return self

    def refresh_initial_conditions(self):
        pass


    def __iter__(self):
        return iter(self.reactions)

@singledispatch
def generate_key_reaction(obj: str | Reaction) -> int:
    raise ValueError(f"{obj} is invalid as an argument to generate_key_reaction. It must be of type str | Reaction")

@generate_key_reaction.register
def _(string: str) -> int:
    if is_string_reaction(string):
        return sum(map(ord,list(string.replace(" ","").upper())))
    raise ValueError(f"{string} is not a valid Reaction. Please check documentation for syntax")

@generate_key_reaction.register
def _(reaction: Reaction) -> int:
    return reaction.key

def generate_name_reaction(string: str)-> str:
    return


if __name__ == "__main__":
    print("")
