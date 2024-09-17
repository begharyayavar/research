import numpy as np
from typing import List

from numba import njit,prange
from numba_progress import ProgressBar

from benchmarks import benchmark,storage

from functions import calculate_propensity

@storage
@benchmark
@njit(nogil=True,parallel=True)
def simulate(   state: np.ndarray,\
                timestamps: np.ndarray,\
                reactions: np.ndarray,\
                reactant_indices: List ,\
                rate_constants: np.ndarray,\
                cycles: int,\
                steps: int,\
                progress: ProgressBar) -> None:

    # Precomputing u1 and u2 outside the main loop
    u1_vals = np.random.random(size=(cycles, steps))
    u2_vals = np.random.random(size=(cycles, steps))

    for cycle in prange(cycles):
        
        for step in range(steps):
        # Calculate updated overall reaction rate
            propensities = np.array(\
                                [calculate_propensity(\
                                    state[cycle,:,:],\
                                    reactant_indices[r],\
                                    step,\
                                    rate_constants[r]) \
                                    
                                        for r in range(len(reactions))])
            
            R = np.sum(propensities)
            
        # Calculate time to next reaction
            tau = 1/R * np.log(1/u1_vals[cycle,step])

        # Store reaction time
            timestamps[cycle, step+1] = timestamps[cycle,step] + tau
        
        # Select which reaction to occur and update populations
            cumulative_propensities_sum = np.cumsum(propensities)

        # Using a cumulative sum to line up propensities and pick a random number to decide which bin it falls into
            for index in range(len(propensities)):
                if u2_vals[cycle,step] <= cumulative_propensities_sum[index]/R:
                    state[cycle,step+1,:] = state[cycle,step,:] + reactions[index]
                    break
        progress.update()
    return
