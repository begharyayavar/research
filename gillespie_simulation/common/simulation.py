from typing import Self

from reaction_parser import parser
from utils import is_file
class Simulation:

    def __init__(self: Self):
        self._simvars : SimulationVariables
        return

    def add_reactions_from_file(self,filepath: str):
        if is_file(filepath):
            self._simvars = parser(filepath)
        else:
            raise ValueError(f"{filepath} is not a valid file")

    def run(self: Self):

        pass

    def config(self: Self):
        pass