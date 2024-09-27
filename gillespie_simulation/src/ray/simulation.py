import numpy as np
import ray
from typing import List,Dict

from numba import njit,prange

from src.base.functions import calculate_propensity



@njit
def calculate_trajectory(   state_slice: np.ndarray,\
                            timestamp_slice: np.ndarray,\
                            reactions: np.ndarray,
                            reactant_indices: List[np.ndarray],
                            rate_constants: np.ndarray,
                            steps: int,):

    u1_vals = np.random.random(size=(steps))
    u2_vals = np.random.random(size=(steps))

    for step in range(steps):
        # Calculate updated overall reaction rate
            propensities = np.array([calculate_propensity(state_slice,reactant_indices[r],step,rate_constants[r]) for r in range(len(reactions))])
            R = np.sum(propensities)

        # Calculate time to next reaction
            tau = 1/R * np.log(1/u1_vals[step])

        # Store reaction time
            timestamp_slice[step+1] = timestamp_slice[step] + tau

        # Select which reaction to occur and update populations
            cumulative_propensities_sum = np.cumsum(propensities)

            for index in range(len(propensities)):
                if u2_vals[step] <= cumulative_propensities_sum[index]/R:
                    state_slice[step+1,:] = state_slice[step,:] + reactions[index]
                    break
###### Main Code Loop ######
@ray.remote
def simulate_parallel(  initial_specie_counts: Dict[int,int],\
                        reactions: np.ndarray,\
                        reactant_indices: List ,\
                        rate_constants: np.ndarray,\
                        steps: int):

    timestamp_slice = np.zeros((steps + 1))
    state_slice = np.zeros((steps + 1,len(initial_specie_counts)))
    for specie in initial_specie_counts:
        state_slice[0,specie] = initial_specie_counts[specie]

    return calculate_trajectory(state_slice,timestamp_slice,reactions,reactant_indices,rate_constants,steps)

def simulate(   reactions: np.ndarray,\
                reactant_indices: List ,\
                rate_constants: np.ndarray,\
                initial_specie_counts: Dict[int,int],\
                cycles: int,\
                steps: int):

    results = []

    for cycle in range(cycles):

        results.append(\
            simulate_parallel.remote(\
                initial_specie_counts,\
                reactions,\
                reactant_indices,\
                rate_constants,\
                steps))

    for result in results:
        ray.get(result)
