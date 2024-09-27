# An implemetation of the Gillespie algorithm
# applied to a pair of reactions:

import numpy as np
import numba as nb
from numba import njit,prange
from numba.typed import Dict as Dictionary
from numba_progress import ProgressBar
from tqdm import tqdm
from typing import List,Dict,Tuple
from time import perf_counter
from common.reaction_parser import reaction_parser
from common.utils import convert_str_to_int
from src.base.functions import   calculate_propensity,\
                        min_difference,\
                        transform_state_to_trajectories,\
                        fill_empty_with_last_value
from common.benchmarks import benchmark,storage
from common.prints import print_status
from common.plots import plot_time,plot_trajectories
from numba.simulation import simulate
# PARAMETERS
# ==============================
np.random.seed(123) # fixing seed for repeatability
NUM_STEPS = 500 # Number of reactions per trajectory
NUM_CYCLES = 50000 # number of trajectories
REACTION_FILE = "reactions2.txt" # Filename where reactions are written
# ==============================

# Initialization
# ==============================
species,\
reactions,\
reactant_indices,\
rate_constants,\
initial_specie_counts = reaction_parser(REACTION_FILE)
# ==============================


timestamps = np.zeros((NUM_CYCLES, NUM_STEPS+1),dtype = TIMESTAMPS_DTYPE)
state = np.zeros((NUM_CYCLES, NUM_STEPS+1,len(species)),dtype = STATE_DTYPE)

# Store initial conditions
for specie in range(len(species)):
    for cycle in range(NUM_CYCLES):
        state[cycle,0,specie] = initial_specie_counts[specie]

###### Main Code Loop ######


print_status("Simulating ...")
with ProgressBar(total=NUM_CYCLES) as progress:
    simulate(state,timestamps,reactions,reactant_indices,rate_constants,NUM_CYCLES,NUM_STEPS,progress)

EPSILON = min_difference(timestamps)
MAX_TIME = timestamps.max() + EPSILON

NUM_AVERAGES = NUM_STEPS
average_timestamps = np.linspace(0, MAX_TIME, NUM_AVERAGES + 1)
trajectories = transform_state_to_trajectories(state)
species_ave = np.zeros((len(species),NUM_AVERAGES+1))

species_numba = Dictionary.empty(nb.char,nb.int64)
for key in species:
    species_numba[convert_str_to_int(key)] = species[key]





bin_indexes,bincounts = bin_timestamps(timestamps,average_timestamps)
step_averages = step_average = np.zeros((NUM_STEPS + 1))
with ProgressBar(total = NUM_STEPS) as progress:
    step_averages = state_average_across_cycles(np.array(list(species.values())),state,bin_indexes,bincounts,progress)
print(step_averages)



# with ProgressBar(total=len(species)) as progress:
#     calculate_averages(species_numba,trajectories,species_ave,progress)

###### Plot Trajectories ######

# plot_time(timestamps,average_timestamps)

# plot_trajectories(species,trajectories,species_ave,timestamps,average_timestamps)

