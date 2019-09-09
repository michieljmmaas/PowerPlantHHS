"""train a single group"""

import numpy as np

N_PANELS = 4
N_SOLAR_FEATURES = N_PANELS * 3
N_WIND_FEATURES = 0  # for now
N_FEATURES = N_SOLAR_FEATURES + N_WIND_FEATURES


def train(n_generations, group_size, simulink_user, cost_calculator, genetic_algorithm,
          surface_min, surface_max, angle_min, angle_max, orientation_min, orientation_max):
    """train genetic algorithm"""

    # generate random values in valid range
    solar_values = np.random.rand(group_size, N_SOLAR_FEATURES)
    solar_values[:, 0::3] *= (surface_max - surface_min)
    solar_values[:, 0::3] += surface_min
    solar_values[:, 1::3] *= (angle_max - angle_min)
    solar_values[:, 1::3] += angle_min
    solar_values[:, 2::3] *= (orientation_max - orientation_min)
    solar_values[:, 2::3] += orientation_min
    # wind_values = np.random.rand([group_size, N_WIND_FEATURES], dtype=np.float)
    # group_values = np.concatenate((solar_values, wind_values), axis=1)  # concatenate on features
    group_values = solar_values  # for now

    # prepare min and max arrays to truncate values later
    highest_allowed = np.zeros_like(group_values)
    lowest_allowed = np.zeros_like(group_values)
    highest_allowed[:, 0:N_SOLAR_FEATURES:3] = surface_max
    lowest_allowed[:, 0:N_SOLAR_FEATURES:3] = surface_min
    highest_allowed[:, 1:N_SOLAR_FEATURES:3] = angle_max
    lowest_allowed[:, 1:N_SOLAR_FEATURES:3] = angle_min
    highest_allowed[:, 2:N_SOLAR_FEATURES:3] = orientation_max
    lowest_allowed[:, 2:N_SOLAR_FEATURES:3] = orientation_min

    last_generation = n_generations - 1
    for generation in range(n_generations):
        # send values to simulink

        # run simulink

        # get values from simulink

        # run cost calculator

        # store intermediate results?

        if generation == last_generation:
            # get result with lowest cost
            result = None  # placeholder
            # return best result
            return result

        # run genetic algorithm

        # update group values

        # remove illegal values
        group_values = np.minimum(group_values, highest_allowed)
        group_values = np.maximum(group_values, lowest_allowed)
        