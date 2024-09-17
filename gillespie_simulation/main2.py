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
from reaction_parser import reaction_parser
from utils import convert_str_to_int
from functions import   calculate_propensity,\
                        min_difference,\
                        transform_state_to_trajectories,\
                        fill_empty_with_last_value
from benchmarks import benchmark,storage
from prints import print_status                  
from plots import plot_time,plot_trajectories
from simulation import simulate
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


TIMESTAMPS_DTYPE = np.float32
STATE_DTYPE = np.uint8
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

@benchmark
def bin_timestamps(timestamps: np.ndarray,average_timestamps: np.ndarray) -> Tuple[np.ndarray,np.ndarray]:
    return np.digitize(timestamps,average_timestamps),np.histogram(timestamps,average_timestamps)[0]  # !IMPORTANT should i write my own digitize implementation for sorted arrays...

@benchmark
def state_average_across_cycles(specie_indexes:np.ndarray,state: np.ndarray,bin_indexes: np.ndarray,bincounts: np.ndarray,progress: ProgressBar) -> np.ndarray: #-> np.ndarray:
    step_average = np.zeros((NUM_STEPS+1,len(specie_indexes)))
    
    # times = []
    for step in prange(1,NUM_STEPS+1,1):
        # t1 = perf_counter()
        mask = bin_indexes == step
        # t2 = perf_counter()
        for specie_index in prange(specie_indexes.max()+1):
            step_sum = np.sum(state[:,:,specie_index][mask])
            # t3 = perf_counter()
            if bincounts[step - 1] > 0:
                step_average[step] = step_sum / bincounts[step - 1]
            else:
                step_average[step] = step_average[step-1]
            # t4 = perf_counter()
        # np.divide(np.sum(np.where(bin_indexes == step,state,zeros)),bincounts[step-1])
            # times.append([t2-t1,t3-t2,t4-t3])
        
        progress.update()
    # average_times = np.sum(times,axis = 0)/(len(times)*len(species))
    # print("Average times")
    # print(f"{average_times}")
    return step_average

@njit(nogil=True,parallel = True)
def state_average_across_cycles_numba(specie_indexes:np.ndarray,state: np.ndarray,bin_indexes: np.ndarray,bincounts: np.ndarray,progress: ProgressBar) -> np.ndarray: #-> np.ndarray:
    step_average = np.zeros((NUM_STEPS+1,len(specie_indexes)))
    
    # times = []
    for step in prange(1,NUM_STEPS+1,1):
        # t1 = perf_counter()
        mask = (bin_indexes == step).ravel()
        # t2 = perf_counter()
        for specie_index in prange(specie_indexes.max()+1):
            step_sum = np.sum(state[:,:,specie_index][mask])
            # t3 = perf_counter()
            if bincounts[step - 1] > 0:
                step_average[step] = step_sum / bincounts[step - 1]
            else:
                step_average[step] = step_average[step-1]
            # t4 = perf_counter()
        # np.divide(np.sum(np.where(bin_indexes == step,state,zeros)),bincounts[step-1])
            # times.append([t2-t1,t3-t2,t4-t3])
        
        progress.update()
    # average_times = np.sum(times,axis = 0)/(len(times)*len(species))
    # print("Average times")
    # print(f"{average_times}")
    return step_average


bin_indexes,bincounts = bin_timestamps(timestamps,average_timestamps)
step_averages = step_average = np.zeros((NUM_STEPS + 1))
with ProgressBar(total = NUM_STEPS) as progress:
    step_averages = state_average_across_cycles(np.array(list(species.values())),state,bin_indexes,bincounts,progress)

print(step_averages)
def plot_step_averages(species,step_averages,timestamps,average_timestamps):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(len(species), 1, figsize=(20,10))
    MAX_X = average_timestamps.max()
    MAX_Y = trajectories.max()
    cycles = trajectories.shape[1]
    
    for specie in species:
        #Title
        axs[species[specie]].set_title(f'Number {specie} Molecules')
        
        # Axis Labels
        axs[species[specie]].set_xlabel("Time")
        axs[species[specie]].set_ylabel("Number of Species")
        
        # Axis Limits
        axs[species[specie]].set_xlim((0,MAX_X))
        axs[species[specie]].set_ylim((0,MAX_Y))
    
        for cycle in range(cycles):
            axs[species[specie]].plot(timestamps[cycle,:], trajectories[species[specie],cycle,:],\
                marker='', color='grey', linewidth=0.6, alpha=0.3)
    
        axs[species[specie]].plot(average_timestamps, step_average.transpose()[species[specie]],\
            marker='', color='red', linewidth=1.9, alpha=0.9)
    plt.show()
    return 

@benchmark
def calculate_averages(species: Dict[str,int],trajectories: np.ndarray,species_ave: np.ndarray,progress: ProgressBar) -> None:
    # Initialize the first step
    for specie in species:
        species_ave[species[specie], 0] = trajectories[species[specie]][0,0]

    # Binning by timestamps into the correct time interval
    bin_indexes,bincount = bin_timestamps(timestamps,average_timestamps)
    
    for specie in tqdm(species):
        for step in tqdm(prange(1,NUM_STEPS+1,1)): # !IMPORTANT unelegant but works. but try to fix? 
            species_ave[species[specie],step] =    np.divide(np.sum(trajectories[species[specie]][bin_indexes == step]),\
                                                    bincount[step-1]) # Should i use floor divide? what makes sense for smaller values?
        fill_empty_with_last_value(species_ave[species[specie]]) # !IMPORTANT figure out whether to fill and then take average or vice versa.I think it's better to take the mean and then fill it.
        progress.update(1)
    
    # Vectorized calculation for each species over all time steps
    return 
# with ProgressBar(total=len(species)) as progress:
#     calculate_averages(species_numba,trajectories,species_ave,progress)

###### Plot Trajectories ######

# plot_time(timestamps,average_timestamps)

# plot_trajectories(species,trajectories,species_ave,timestamps,average_timestamps)

