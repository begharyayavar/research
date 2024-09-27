from common.benchmarks import benchmark
import numpy as np


@benchmark
def state_average_across_cycles(metadata: Metadata,state: np.ndarray,timestamps: np.ndarray) -> np.ndarray:
    step_average = np.zeros((metadata.steps+1,metadata.num_species))

    bin_indexes =

    for cycle in bin_indexes:
        for step in cycle:
            for specie_index in specie_indexes:
                step_average[bin_indexes[cycle,step],specie_index]+= state[cycle,step,specie_index]
    step_average/= bincounts

    return step_average



@benchmark
def trajectory_average_across_cycles(species: Dict[str,int],trajectories: np.ndarray,species_ave: np.ndarray) -> np.ndarray:
    # Initialize the first step
    species_average =
    for specie in species:
        species_ave[species[specie], 0] = trajectories[species[specie]][0,0]

    # Binning by timestamps into the correct time interval
    bin_indexes,_ = bin_timestamps(timestamps,average_timestamps)

    for specie in tqdm(species):
        for step in tqdm(prange(1,NUM_STEPS+1,1)): # !IMPORTANT unelegant but works. but try to fix?
            species_ave[species[specie],step] =    np.mean(trajectories[species[specie]][bin_indexes == step]) # Should i use floor divide? what makes sense for smaller values?
        fill_empty_with_last_value(species_ave[species[specie]]) # !IMPORTANT figure out whether to fill and then take average or vice versa.I think it's better to take the mean and then fill it.
        progress.update(1)

    # Vectorized calculation for each species over all time steps
    return