from numba import njit
import numpy as np
import numpy.typing as npt
from typing import Any


@njit
def transform_state_to_trajectories(state: np.ndarray) -> np.ndarray:
    return np.transpose(state,axes = (2,0,1))

@njit
def min_difference(array: npt.NDArray) -> Any:
    temp = np.diff(np.sort(array)).flatten()
    return temp[temp>0].min()

def fill_empty_helper(mask:np.ndarray,idx: np.ndarray,n_dims: int) -> tuple[np.ndarray, ...]: # !IMPORTANT fuck me but it works. soooo ugly tho. try to fix. eventually.
                arg_list =[np.nonzero(mask)[i] for i in range(n_dims-1)]
                arg_list.append(idx[mask])
                return tuple(arg_list)

def fill_empty_with_last_value(nan_matrix: np.ndarray,row_axis: int = 0) -> np.ndarray: # !IMPORTANT write documentation for this you will definitely forget how this works.
            mask = np.isnan(nan_matrix)
            idx = np.where(~mask,np.arange(mask.shape[row_axis]),0)
            np.maximum.accumulate(idx,axis=row_axis, out=idx)
            nan_matrix[mask] = nan_matrix[fill_empty_helper(mask,idx,len(nan_matrix.shape))]
            return nan_matrix

@njit
def calculate_propensity(   state_slice:np.ndarray,\
                            specie_indexes: np.ndarray,\
                            step: int,\
                            Rf: np.floating)\
                                -> np.floating:

    return Rf * np.prod(state_slice[step ,:][specie_indexes])

@benchmark
def bin_timestamps(timestamps: np.ndarray,average_timestamps: np.ndarray) -> Tuple[np.ndarray,np.ndarray]:
    return np.digitize(timestamps,average_timestamps),np.histogram(timestamps,average_timestamps)[0]  # !IMPORTANT should i write my own digitize implementation for sorted arrays...
