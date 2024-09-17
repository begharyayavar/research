import matplotlib.pyplot as plt
import numpy as np
from typing import Dict

def plot_time(timestamps: np.ndarray,average_timestamps: np.ndarray,show_plots: bool = False,save_plots: bool = False) -> None:
    NUM_CYCLES = timestamps.shape[0]
    fig, axs = plt.subplots(1, 1, figsize=(20,20))
    axs.set_title('Passage of time')
    axs.plot(average_timestamps, np.average(timestamps,axis = 0), marker='', color='blue', linewidth=1.9, alpha=0.9)
    axs.plot(average_timestamps, average_timestamps, marker='', color='red', linewidth=1.9, alpha=0.9)

    for cycle in range(NUM_CYCLES):
        axs.plot(average_timestamps,timestamps[cycle,:], marker='', color='grey', linewidth=0.6, alpha=0.3)
    axs.set_aspect('equal', adjustable='box')
    if show_plots:
        plt.show()
    return

def plot_trajectories(  species: Dict[str,int],\
                        trajectories: np.ndarray,\
                        species_average: np.ndarray,\
                        timestamps: np.ndarray,\
                        average_timestamps: np.ndarray,\
                        show_plots: bool = False,\
                        save_plots: bool = False) -> None: # ?WEIRD Funny naming. I'll get to it.
    
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
    
        axs[species[specie]].plot(average_timestamps, species_average[species[specie]],\
            marker='', color='red', linewidth=1.9, alpha=0.9)
    if show_plots:    
        plt.show()
    return 