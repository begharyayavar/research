import numpy as np
from typing import List
from dataclasses import dataclass


@dataclass
class ReactionH:
    index: int
    reactants: List[str]
    products: List[str]
    Rf: np.floating
    coefficients: np.ndarray
    reactant_indices: np.ndarray
    product_indices: np.ndarray

