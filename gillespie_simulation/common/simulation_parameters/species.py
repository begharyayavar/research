from typing import Dict,Self,Any,List
from collections.abc import Iterable
from manager import SpecieKey,SpecieIndex
from dataclasses import dataclass
from utils import convert_str_to_int
from itertools import chain

@dataclass(frozen=True)
class Specie:
    name: str
    key: int

    def __repr__(self: "Specie"):
        return f"{self.name}"

def specie_factory(obj: str | Specie) -> Specie:
    if isinstance(obj,str):
        if is_substring_specie(obj):
            return Specie(obj,generate_key_specie(obj))
        else:
            raise ValueError(f"{obj} is not a valid Specie. Please check documentation for syntax")
    if isinstance(obj,Specie):
        return obj
    raise TypeError(f"{obj} is not of type 'str | Specie'")

@dataclass(frozen=True)
class Species:

    species: Iterable[Specie]

    def __iter__(self: "Species"):
        return iter(self.species)

    def __add__(self: "Species",species: "Species") -> "Species":
        return species_factory(chain(self.species,species.species))

    def __repr__(self: "Species") -> str:
        return f"{self.species}"

def species_factory(obj : Species |Iterable[Specie] | Iterable[str] ) -> Species:
    if isinstance(obj,Species):
        return obj
    if all(map(lambda x: isinstance(x,Specie),obj)):
        return Species(tuple(obj))
    if all(map(lambda x: isinstance(x,str),obj)):
        return Species([specie_factory(value) for value in obj])
    raise TypeError(f"{obj} is not of type 'str | Specie'")


## Helper Functions

def generate_key_specie(obj: str | Specie) -> int:
    if isinstance(obj,Specie):
        return obj.key
    if is_substring_specie(obj):
        return convert_str_to_int(str(obj))
    else:
        raise ValueError(f"{obj} is not a valid Specie. Please check documentation for syntax")

def is_substring_specie(string: str) -> bool:
    return all([character in ALPHABET+NUMBERS for character in string])\
            and string[0] in ALPHABET
