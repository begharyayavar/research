from typing import Self

from common.configuration import DEFAULT_CYCLES,DEFAULT_STEPS

from reaction_parser import reaction_parser
from utils import is_file
class Simulation:
    def __init__(self: Self,cycles: int = DEFAULT_CYCLES,steps: int = DEFAULT_STEPS):
        self.cycles = cycles
        self.steps = steps
        self.simulation_parameters = SimulationParameters()

    def add_reaction(self: Self,string: str) -> None:

        if is_file(string):
            pass

    def add_initial_conditions(self: Self,string: str) -> None:
        pass

    def set_simulation_parameters(self: Self):

    def run(self: Self):


        pass

    def config(self: Self):
        pass