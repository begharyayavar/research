from typing import List,Dict,Tuple,Set,Iterable
import numpy as np


from reactions import ReactionH

from configuration import REACTION_DELIMITERS,REACTANT_DELIMITERS,RATE_CONSTANT_DELIMITERS,INITIAL_CONDITION_DELIMITERS,ALL_DELIMITERS
from utils import prep_line,split_multiple,is_substring_species,is_string_initial_condition,is_string_reaction,is_string_number
from prints import print_species,print_reactions,print_initial_conditions,print_status

def calculate_specie_indices(species_list: List[str],species: Dict[str,int]):
    return np.array([species[specie] for specie in species_list])

def assign_species_id(species_list: Iterable[str]) -> Dict[str,int]:
    temp_list = sorted(list(set(species_list)))    
    return {temp_list[i]:i for i in range(len(temp_list))}

def parse_reaction(index: int,reaction_string: str,species: Dict[str,int]) -> ReactionH:
    reactants = parse_reactants(reaction_string)
    products = parse_products(reaction_string)
    Rf = parse_Rf(reaction_string)
    coefficients = parse_coefficients(reaction_string,species)
    reactant_indicies = calculate_specie_indices(reactants,species)
    product_indicies = calculate_specie_indices(products,species)

    return ReactionH(index,reactants,products,Rf,coefficients,reactant_indicies,product_indicies)

def parse_reactants(reaction_string: str) -> List[str]:
    temp_str = split_multiple(reaction_string,REACTION_DELIMITERS)[0]
    temp_list = split_multiple(temp_str,REACTANT_DELIMITERS)
    return list(filter(lambda x: is_substring_species(x),temp_list))

def parse_products(reaction_string: str) -> List[str]:
    temp_str = split_multiple(reaction_string,REACTION_DELIMITERS)[1]
    temp2_str = split_multiple(temp_str,RATE_CONSTANT_DELIMITERS)[0]
    temp_list = split_multiple(temp2_str,REACTANT_DELIMITERS)
    return list(filter(lambda x: is_substring_species(x),temp_list))

def parse_Rf(reaction_string: str) -> np.floating:
    temp2_str = split_multiple(reaction_string,RATE_CONSTANT_DELIMITERS)[1]
    return np.float_(temp2_str)

def parse_coefficients(reaction_string: str,species: Dict[str,int]) -> np.ndarray:
    temp_str = split_multiple(reaction_string,RATE_CONSTANT_DELIMITERS)[0]
    temp_list = split_multiple(temp_str,REACTION_DELIMITERS)
    temp_reactants = split_multiple(temp_list[0],REACTANT_DELIMITERS)
    temp_products = split_multiple(temp_list[1],REACTANT_DELIMITERS)
    
    temp_array = np.zeros(shape=(len(species)))

    # Defaults for no given coefficient
    for i in temp_reactants:
        if i in species:
            temp_array[species[i]] = -1
    
    for i in temp_products:
        if i in species:
            temp_array[species[i]] = 1

    for i in range(len(temp_reactants)):
        if is_string_number(temp_reactants[i]):
            if i+1<len(temp_reactants):
                if is_substring_species(temp_reactants[i+1]):
                    temp_array[species[temp_reactants[i+1]]] = -int(temp_reactants[i])              
    
    for i in range(len(temp_products)):
        if is_string_number(temp_products[i]):
            if i+1<len(temp_products):
                if is_substring_species(temp_products[i+1]):
                    temp_array[species[temp_products[i+1]]] = int(temp_products[i])
    
    return temp_array

def parse_species(reaction_string: str) -> Iterable[str]:
    species: Set[str] = set()
    all_characters: List[str] = split_multiple(reaction_string,ALL_DELIMITERS)
    for characters in all_characters:
        if is_substring_species(characters):
            species.add(characters)
    return species

def parse_initial_conditions(reaction_string: str,species: Dict[str,int]) -> Dict[int,int]:
    temp = split_multiple(reaction_string,INITIAL_CONDITION_DELIMITERS)
    if temp[0] not in species:
        raise ValueError(f"Unknown Species while setting initial conditions: {temp[0]}")
    return {species[temp[0]]:int(temp[1])}

def reaction_parser(filename: str,logging: bool = True)\
        ->  Tuple[Dict[str,int],np.ndarray,List[int],np.ndarray,Dict[int,int]]:
    with open(filename,"r") as f:
        
        if logging:        
            print_status(f"Parsing {filename} ...\n")
        
        # Parse Species
        temp: Set[str] = set()
        for line in f:
            base: str = prep_line(line)
            temp.update(parse_species(base))
        
        species: Dict[str,int] = assign_species_id(temp)
        
        if logging:
            print_species(species)
        f.seek(0)
        
        # Parse Reactions
        temp2 = []
        curr_reaction_index = 0     
        for line in f:
            base: str = line.replace(" ","").split(";")[0]      
            if is_string_reaction(base):
                temp2.append(parse_reaction(curr_reaction_index,base,species))
                curr_reaction_index+=1
        reactionsh = [reactionh for reactionh in temp2]

        # To ensure index matches
        reactions = np.zeros((curr_reaction_index,len(species)))
        rate_constants = np.zeros((curr_reaction_index))
        reactant_indices = [0]*curr_reaction_index

        for i in reactionsh:
            reactions[i.index] = i.coefficients
            rate_constants[i.index] = i.Rf
            reactant_indices[i.index] = i.reactant_indices
        
        if logging:
            print_reactions(reactionsh,species)
        f.seek(0)       
        
        # Parse Initial Conditions
        temp3 = {}
        for line in f:    
            base: str = prep_line(line)
            if is_string_initial_condition(base):
                temp3.update(parse_initial_conditions(base,species))
        for specie in species: # Filling in blank initial conditions
            if species[specie] not in temp3:
                temp3[species[specie]] = 0        
        
        intial_conditions: Dict[int,int] = {specie:temp3[specie] for specie in temp3}        
        
        if logging:
            print_initial_conditions(intial_conditions,species)
        
        del temp,temp2,temp3
        return species,reactions,reactant_indices,rate_constants,intial_conditions