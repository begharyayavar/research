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