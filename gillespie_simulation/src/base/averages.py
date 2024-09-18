from benchmarks import benchmark
from numba import njit, prange
import numpy as np


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

@benchmark
def calculate_averages(species: Dict[str,int],trajectories: np.ndarray,species_ave: np.ndarray,progress: ProgressBar) -> None:
    # Initialize the first step
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