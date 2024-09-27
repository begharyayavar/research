from typing import List,Dict,Tuple,Set,Iterable
import numpy as np

from configuration import REACTION_DELIMITERS,REACTANT_DELIMITERS,RATE_CONSTANT_DELIMITERS,INITIAL_CONDITION_DELIMITERS,ALL_DELIMITERS
from utils import prep_line,split_multiple,is_substring_species,is_string_initial_condition,is_string_reaction,is_string_number
# from prints import print_species,print_reactions,print_initial_conditions,print_status

def parse_species(reaction_string: str) -> Iterable[str]:
    base = prep_line(reaction_string)
    species: Set[str] = set()
    all_characters: List[str] = split_multiple(base,ALL_DELIMITERS)
    for characters in all_characters:
        if is_substring_species(characters):
            species.add(characters)
    return species

def calculate_specie_indices(species_list: List[str],species: Dict[str,int]):
    return np.array([species[specie] for specie in species_list])

def assign_species_id(species_list: Iterable[str]) -> Dict[str,int]:
    temp_list = sorted(list(set(species_list)))
    return {temp_list[i]:i for i in range(len(temp_list))}

def parse_reaction(reaction_string: str):
    base = reaction_string.replace(" ","").split(";")[0]

    reactants = parse_reactants(reaction_string)
    products = parse_products(reaction_string)
    Rf = parse_Rf(reaction_string)
    coefficients = parse_coefficients(reaction_string)

    return reactants,products,Rf,coefficients

def parse_reactants(reaction_string: str) -> List[str]:
    base = reaction_string.replace(" ","").split(";")[0]
    temp_str = split_multiple(base,REACTION_DELIMITERS)[0]
    temp_list = split_multiple(temp_str,REACTANT_DELIMITERS)
    return list(filter(is_substring_species,temp_list))

def parse_products(reaction_string: str) -> List[str]:
    base = reaction_string.replace(" ","").split(";")[0]
    temp_str = split_multiple(base,REACTION_DELIMITERS)[1]
    temp2_str = split_multiple(temp_str,RATE_CONSTANT_DELIMITERS)[0]
    temp_list = split_multiple(temp2_str,REACTANT_DELIMITERS)
    return list(filter(is_substring_species,temp_list))

def parse_Rf(reaction_string: str) -> float:
    base = reaction_string.replace(" ","").split(";")[0]
    temp2_str = split_multiple(base,RATE_CONSTANT_DELIMITERS)[1]
    return float(temp2_str)

def parse_coefficients(reaction_string: str) -> Dict[str,int]:
    species = parse_species(reaction_string)
    base = reaction_string.replace(" ","").split(";")[0]
    temp_str = split_multiple(base,RATE_CONSTANT_DELIMITERS)[0]
    temp_list = split_multiple(temp_str,REACTION_DELIMITERS)
    temp_reactants = split_multiple(temp_list[0],REACTANT_DELIMITERS)
    temp_products = split_multiple(temp_list[1],REACTANT_DELIMITERS)

    temp_dict = {specie:1 for specie in species}

    # Defaults for no given coefficient
    for i in temp_reactants:
        if i in species:
            temp_dict[i] = 1

    for i in temp_products:
        if i in species:
            temp_dict[i] = 1


    for i in range(len(temp_reactants)):
        if is_string_number(temp_reactants[i]):
            if i+1<len(temp_reactants):
                if is_substring_species(temp_reactants[i+1]):
                    temp_dict[temp_reactants[i+1]] = int(temp_reactants[i])

    for i in range(len(temp_products)):
        if is_string_number(temp_products[i]):
            if i+1<len(temp_products):
                if is_substring_species(temp_products[i+1]):
                    temp_dict[temp_products[i+1]] = int(temp_products[i])

    return temp_dict

def parse_initial_conditions(reaction_string: str,species: Dict[str,int]) -> Dict[int,int]:
    base = prep_line(reaction_string)
    temp = split_multiple(base,INITIAL_CONDITION_DELIMITERS)
    if temp[0] not in species:
        raise ValueError(f"Unknown Species while setting initial conditions: {temp[0]}")
    return {species[temp[0]]:int(temp[1])}

def parser(filename: str,logging: bool = True)\
        ->  Tuple[Dict[str,int],np.ndarray,List[int],np.ndarray,Dict[int,int]]:
    with open(filename,"r",encoding="utf-8") as f:
        if logging:
            print_status(f"Parsing {filename} ...\n")

        # Parse Reactions
        temp = []
        for line in f:
            if is_string_reaction(line):
                temp.append(parse_reaction(line))
        reactions = [reaction for reaction in temp]

        if logging:
            print_reactions(reactions)
        f.seek(0)

        # Parse Initial Conditions
        temp2 = {}
        for line in f:
            if is_string_initial_condition(line):
                temp2.update(parse_initial_conditions(line))

        intial_conditions = InitialConditions(temp2)

        if logging:
            print_initial_conditions(intial_conditions)

        del temp,temp2
        return reactions,intial_conditions