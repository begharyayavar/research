from typing import List,Generator
from configuration import REACTION_DELIMITERS,INITIAL_CONDITION_DELIMITERS,DEFAULT_TAB_WIDTH,DEFAULT_COL_WIDTH,ALPHABET,NUMBERS



def prep_line(string: str)-> str:
    return remove_whitespace(string).split(";")[0]

def remove_whitespace(string: str) -> str:
    return "".join(string.replace(" ",""))

def split_multiple(string: str, delimiters: List["str"]) -> List[str]:
    for delimiter in delimiters:
        string = " ".join(string.split(delimiter))
    return string.split()

def is_string_number(string: str) -> bool:
    return all([character in NUMBERS for character in string])



def convert_str_to_int(string: str) -> int:
    return int("".join([str(ord(char)) for char in string]))

def is_string_reaction(string: str) -> bool:
    base: str = string.replace(" ","").split(";")[0]
    return any([char in base for char in REACTION_DELIMITERS])

def is_string_initial_condition(string: str) -> bool:
    return any([char in string for char in INITIAL_CONDITION_DELIMITERS])

def size_as_string(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{str(round(num,2))} {unit}{suffix}"
        num /= 1024.0
    return f"{str(round(num,2))}Yi{suffix}"

# MAX_NUM_REACTIONS = 100
# def reaction_index_generator() -> Generator[int]:
#     for index in range(MAX_NUM_REACTIONS):
#         yield index

# MAX_NUM_SPECIES = 500
# def specie_index_generator() -> Generator[int]:
#     for index in range(MAX_NUM_SPECIES):
#         yield index


def pad_with_tabs(string: str,width = DEFAULT_COL_WIDTH) -> str:
    num_tabs = (width-len(string))//DEFAULT_TAB_WIDTH + (1 if (len(string)% DEFAULT_TAB_WIDTH) >= 1 else 0)
    tabs = "\t"*num_tabs
    return f"{string}{tabs}"
