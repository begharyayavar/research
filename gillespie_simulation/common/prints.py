from typing import Any,Dict,Set,List,Iterable,Callable
from reactions import ReactionH
from configuration import *
import inspect
from utils import size_as_string,pad_with_tabs

def print_heading(string: str) -> None:
    print(f"{RESET}{HEADING_COLOR}{BOLD}\n\n\t{string}\n{RESET}")

def print_line() -> None:
    print(f"\n\t{RESET}{LINE_COLOR}================================================== \n{RESET}")

def print_species(species: Dict[str,int]) -> None:
    print_heading("Species")
    print(f"{RESET}\n\t{list(species.keys())}{RESET}")
    print_line()
    
def print_reactions(reactionsh: List[ReactionH],species: Dict[str,int]) -> None:
    print_heading("Reactions")
    print(f"\n\t{species}\n")
    for reactionh in reactionsh:
        print(  f"\t{RESET}{REACTANT_COLOR}{reactionh.reactants}{RESET} ->  " +\
                    f"{RESET}{PRODUCT_COLOR}{reactionh.products}{RESET} @ " +\
                        f"{RESET}{COUNT_COLOR} {reactionh.Rf} {RESET}")
        print(f"{RESET}{TEXT_COLOR}\tCoefficients = {RESET}{reactionh.coefficients}\n")
    print_line()
    pass

def print_initial_conditions(initial_conditions: Dict[int,int],species: Dict[str,int]) -> None:
    temp = {specie:initial_conditions[species[specie]] for specie in species}
    print_heading("Initial Conditions")
    print(f"{RESET}")
    for specie in temp:
        print(f"{RESET}{PRODUCT_COLOR}\t{pad_with_tabs(specie)}{RESET}:\t {RESET}{COUNT_COLOR} {temp[specie]} {RESET}")
    print_line()
    
def print_status(string: str) -> None:
    print(f"{RESET}{STATUS_COLOR}{BOLD}\n\n\t{string}\n{RESET}")
    
def print_benchmark(func: Callable,time_taken: float,*args: Any,**kwargs: Any) -> None:
    print_status("Benchmark")
    print(f"\n\t{RESET}{TEXT_COLOR}Time taken for : {RESET}{PRODUCT_COLOR}{func.__name__}{RESET}")
    print(f"\n\t{RESET}{COUNT_COLOR}{time_taken}{RESET}")
    print(f"\n\t{RESET}{TEXT_COLOR}With arguments :{RESET}")
    arguments = f"\n\t".join(list(inspect.signature(func).parameters))
    print(f"\t{RESET}{REACTANT_COLOR}{arguments}{RESET}")
    print_line()
    return

def print_storage(func: Callable,storage_values: Dict[str,int]) -> None:
    print_status("Memory")
    print(f"\n\t{RESET}{TEXT_COLOR}Memory taken for parameters of : {RESET}{PRODUCT_COLOR}{func.__name__}{RESET}")
    print(f"\n\t{RESET}{COUNT_COLOR} {size_as_string(sum(storage_values.values()))}{RESET}\n")
    print(f"\n\t{RESET}{TEXT_COLOR}With arguments :{RESET}")
    for parameter_name in storage_values:
        print(  f"\t{RESET}{REACTANT_COLOR}{pad_with_tabs(parameter_name)}{RESET}:\t " +\
                    f"{RESET}{COUNT_COLOR} {size_as_string(storage_values[parameter_name])} {RESET}")
    print_line()
    return