# ==========================================================
# Initial attemps to initialise so i can understand what i want my interfaces to look like.


# steps = NUM_STEPS   # Number of reactions per trajectory
# cycles = NUM_CYCLES  # Number of trajectories iterated over

# # Set up holder arrays
# species = {"A":0,"B":1,"AB":2}
# initial_specie_counts = {0:35,1:25,2:5}

# reactionh1 = ReactionH(0,["A","B"],["AB"],np.float_(2),np.array([-1,-1,1]),np.array([0,1]),np.array([2]))
# reactionh2 = ReactionH(1,["AB"],["A","B"],np.float_(1),np.array([1,1,-1]),np.array([2]),np.array([0,1]))

# reactionsh: List[ReactionH] = [reactionh1,reactionh2]

# reaction1 = np.array([-1,-1,1])
# reaction2 = np.array([1,1,-1])
# reactions = np.array([reaction1,reaction2])

# reactant1_indices = np.array([0,1])
# reactant2_indices = np.array([2])

# reactant_indices = [reactant1_indices,reactant2_indices]

# rate_constants = np.array([2,1])

# print(state)
# print(trajectories)

# # Pre-allocate

# # Set up average arrays
# T_ave = np.linspace(0, T_max, ave_steps + 1)

# steps = NUM_STEPS   # Number of reactions per trajectory
# cycles = NUM_CYCLES  # Number of trajectories iterated over

# # Set up holder arrays
# species = {"A":0,"B":1,"AB":2}
# initial_specie_counts = {0:35,1:25,2:5}

# reactionh1 = ReactionH(0,["A","B"],["AB"],np.float_(2),np.array([-1,-1,1]),np.array([0,1]),np.array([2]))
# reactionh2 = ReactionH(1,["AB"],["A","B"],np.float_(1),np.array([1,1,-1]),np.array([2]),np.array([0,1]))

# reactionsh: List[ReactionH] = [reactionh1,reactionh2]

# reaction1 = np.array([-1,-1,1])
# reaction2 = np.array([1,1,-1])
# reactions = np.array([reaction1,reaction2])

# reactant1_indices = np.array([0,1])
# reactant2_indices = np.array([2])

# reactant_indices = [reactant1_indices,reactant2_indices]

# rate_constants = np.array([2,1])


# ============================================
# Failed attempts at understanding binning.
    # temp_mask = np.repeat(np.reshape(average_timestamps,(1,-1)),NUM_CYCLES,axis=0)
    # temp2_mask = np.array(temp_mask[:,:]);temp2_mask[:,1:] = temp_mask[:,:-1];temp2_mask[:,0] = temp_mask[:,0];    
    # mask = (temp_mask>=timestamps)&(temp2_mask<=timestamps) 
    # 
    ## what i was trying to do was compare between the current value and the next value
    # what i didn't realise was the values dont have to fall in the next bin
    
    # print(temp_mask) 
    # print("\n")
    # print(temp2_mask)
    # print("\n")
    # print(timestamps)
    # print("\n")
    # print(temp2_mask<=timestamps)
    # print("\n")
    # print(-temp2_mask+timestamps)
    # print("\n")
    # print(temp_mask>=timestamps)
    # print("\n")
    # print(temp_mask-timestamps)
    # print("\n")
    # print(mask)
    # print("\n")
    # print(timestamps*mask)

    # mask = np.array((timestamps[:, :] <= curr_tmax) & (timestamps[:, 1:] > curr_tmax))
    
    # for specie in species:
        
    #     valid_values = (trajectories[species[specie]] * mask)
    #     valid_values[valid_values == 0] = np.nan
    #     # print(mask)
    #     # print(np.nanmean(valid_values,axis = 0))
    #     species_ave[species[specie]] = np.nanmean(valid_values,axis = 0)
        
    #     del valid_values
        # fill_empty_with_last_value(valid_values,1)
        # print("reference passing test")
        # print(valid_values)
        # print(species_ave[species[specie]])
    # print(species_ave)

    # Trying to log performance and trying to figure out if can use masking. i had to use binning...
    
    # # Mask to find the steps where T crosses the current tmax for all cycles
    #     print(np.shape(mask))
    #     t_count = np.sum(mask, axis=1)
    #     t2= perf_counter()
    # # If no samples found, just copy the previous values
    #     if np.all(t_count == 0):
    #         species_ave[:, step] = species_ave[:, step-1]
    #     else:
    # # Sum over valid steps
    #         for specie in species:
    #             t3 = perf_counter()
    #             specie_id = species[specie]
    #             t4 = perf_counter()
    #             specie_sums = np.sum(trajectories[specie_id, :, :-1] * mask, axis=1)
    #             t5 = perf_counter()
    #             species_ave[specie_id, step] = np.sum(specie_sums) / np.sum(t_count)
    #             t6 = perf_counter()
    #             print(f"over valid steps: {t4-t3} {t5-t4} {t6-t5}")
    #     t7 = perf_counter()
    #     print(f"Initial times: {t2 - t1}")
    #     print(f"final_step: {t7-t2}")
    # return trajectories,species_ave

# =====================================================
# failed plots

# print(np.average(timestamps,axis = 0))
# print(average_timestamps)
# Time plot
# axs[1].set_ylim(max_time)
# axs[1].set_xlim(max_time)
# # # Plot average trajectories

# axs[1].plot(average_timestamps, species_ave[1], marker='', color='red', linewidth=1.9, alpha=0.9)
# axs[1].set_title('Number B Molecules')
# axs[1].set_ylim((0,35))
# axs[1].set_xlim((0,0.125))
# axs[2].plot(average_timestamps, species_ave[2], marker='', color='red', linewidth=1.9, alpha=0.9)
# axs[2].set_title('Number AB Molecules')
# axs[2].set_xlabel("Time")
# axs[2].set_ylim((0,35))
# axs[2].set_xlim((0,0.125))

# # Plot each simulated trajectory
# for cycle in range(NUM_CYCLES):
    # axs[0].plot(average_timestamps,timestamps[cycle,:], marker='', color='grey', linewidth=0.6, alpha=0.3)
    # axs[0].plot(average_timestamps,timestamps[cycle,:], marker='', color='grey', linewidth=0.6, alpha=0.3)
    # axs[2].plot(average_timestamps,timestamps[cycle,:], marker='', color='grey', linewidth=0.6, alpha=0.3)

    # print(state[cycle,:,0])
    # print(timestamps[cycle,:])


# =====================================================
# numba test

# An implenetation of the Gillespie algorithm
# # applied to a pair of reactions:
# # A + B -> AB
# # AB -> A + B

# import numpy as np
# import matplotlib.pyplot as plt
# from numba import njit
# from dataclasses import dataclass
# from typing import List

# # Fix random seed for repeatability
# np.random.seed(123)

# NUM_STEPS = 100
# NUM_CYCLES = 1

# steps = NUM_STEPS   # Number of reactions per trajectory
# cycles = NUM_CYCLES  # Number of trajectories iterated over

# # Set up holder arrays
# species = {"A":0,"B":1,"AB":2}
# initial_specie_counts = {0:35,1:25,2:5}


# @dataclass
# class ReactionH:
#     reactants: List[str]
#     products: List[str]
#     Rf: np.floating
#     coefficients: np.ndarray
#     mask: np.ndarray

# reactionh1 = ReactionH(["A","B"],["AB"],np.float_(2),np.array([-1,-1,1]),np.array([0,1]))
# reactionh2 = ReactionH(["AB"],["A","B"],np.float_(1),np.array([1,1,-1]),np.array([2]))

# reactionsh: List[ReactionH] = [reactionh1,reactionh2]

# reaction1 = np.array([-1,-1,1])
# reaction2 = np.array([1,1,-1])
# reactions = np.array([reaction1,reaction2])

# reactant1_indices = np.array([0,1])
# reactant2_indices = np.array([2])

# reactant_indices = [reactant1_indices,reactant2_indices]

# rate_constants = np.array([2,1])

# @njit
# def calculate_propensity(   state:np.ndarray,\
#                             specie_indexes: np.ndarray,\
#                             cycle: int,\
#                             step: int,\
#                             Rf: np.floating)\
#                                 -> np.floating:

#     return Rf * np.prod(state[cycle ,step ,:][specie_indexes])

# timestamps = np.zeros((cycles, steps+1))
# state = np.zeros((cycles, steps+1,len(species)))

# # Store initial conditions
# for specie in range(len(species)):
#     for cycle in range(cycles):
#         state[cycle,0,specie] = initial_specie_counts[specie]

# ###### Main Code Loop ######
# @njit
# def simulate(   state: np.ndarray,\
#                 timestamps: np.ndarray,\
#                 reactions: np.ndarray,\
#                 reactant_indices: List ,\
#                 rate_constants: np.ndarray,\
#                 cycles: int,\
#                 steps: int):

#     # Precomputing u1 and u2 outside the main loop
#     u1_vals = np.random.random(size=(cycles, steps))
#     u2_vals = np.random.random(size=(cycles, steps))

#     for cycle in range(cycles):
#         for step in range(steps):
#         # Calculate updated overall reaction rate
#             propensities = np.array(\
#                                 [calculate_propensity(\
#                                     state,\
#                                     reactant_indices[r],\
#                                     cycle,\
#                                     step,\
#                                     rate_constants[r]) \
                                    
#                                         for r in range(len(reactions))])
            
#             R = np.sum(propensities)
            
#         # Calculate time to next reaction
#             tau = 1/R * np.log(1/u1_vals[cycle,step])

#         # Store reaction time
#             timestamps[cycle, step+1] = timestamps[cycle,step] + tau
        
#         # Select which reaction to occur and update populations
#             cumulative_propensities_sum = np.cumsum(propensities)

#             for index in range(len(propensities)):
#                 if u2_vals[cycle,step] <= cumulative_propensities_sum[index]/R:
#                     state[cycle,step+1,:] = state[cycle,step,:] + reactions[index]
#                     break


# simulate(state,timestamps,reactions,reactant_indices,rate_constants,cycles,steps)
# # # Pre-allocate
# # ave_steps = NUM_STEPS
# # T_max = T.max()

# # # Set up average arrays
# # T_ave = np.linspace(0, T_max, ave_steps + 1)
# # species_ave = np.zeros((len(species), ave_steps + 1))

# # # Initialize the first step
# # for s in species:
# #     species_ave[species[s], 0] = initial_specie_counts[species[s]]

# # # Vectorized calculation for each species over all time steps
# # for i in range(1, ave_steps + 1):
# #     tmax = T_ave[i]
    
# #     # Mask to find the steps where T crosses the current tmax for all cycles
# #     mask = (T[:, :-1] <= tmax) & (T[:, 1:] > tmax)
# #     t_count = np.sum(mask, axis=1)
    
# #     # If no samples found, just copy the previous values
# #     if np.all(t_count == 0):
# #         species_ave[:, i] = species_ave[:, i-1]
# #     else:
# #         # Sum over valid steps
# #         for s in species:
# #             specie_idx = species[s]
# #             specie_sums = np.sum(counts[specie_idx, :, :-1] * mask, axis=1)
# #             species_ave[specie_idx, i] = np.sum(specie_sums) / np.sum(t_count) if np.sum(t_count) != 0 else species_ave[specie_idx, i-1]

    
# # ###### Plot Trajectories ######
# fig, axs = plt.subplots(3, 1, figsize=(10,20))
# # # Plot average trajectories
# # axs[0].plot(T_ave, species_ave[0], marker='', color='red', linewidth=1.9, alpha=0.9)
# axs[0].set_title('Number A Molecules')
# axs[0].set_ylim((0,35))
# axs[0].set_xlim((0,0.125))
# # axs[1].plot(T_ave, species_ave[1], marker='', color='red', linewidth=1.9, alpha=0.9)
# axs[1].set_title('Number B Molecules')
# axs[1].set_ylim((0,35))
# axs[1].set_xlim((0,0.125))
# # axs[2].plot(T_ave, species_ave[2], marker='', color='red', linewidth=1.9, alpha=0.9)
# axs[2].set_title('Number AB Molecules')
# axs[2].set_xlabel("Time")
# axs[2].set_ylim((0,35))
# axs[2].set_xlim((0,0.125))

# # Plot each simulated trajectory
# for cycle in range(cycles):
#     axs[0].plot(timestamps[cycle,:], state[cycle,:,0], marker='', color='grey', linewidth=0.6, alpha=0.3)
#     axs[1].plot(timestamps[cycle,:], state[cycle,:,1], marker='', color='grey', linewidth=0.6, alpha=0.3)
#     axs[2].plot(timestamps[cycle,:], state[cycle,:,2], marker='', color='grey', linewidth=0.6, alpha=0.3)

#     print(state[cycle,:,0])
#     print(timestamps[cycle,:])
# plt.show()