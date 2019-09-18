"""calculate the cost of panels, windmills and storage"""

import numpy as np
from copy import copy
#from numba import njit

"""
@njit
def _calculate_cost_njit(kwh_array, sp_sm, wm_m,
        target_kw, sp_cost_per_sm, wm_cost_per_m, st_cost_per_kwh, deficit_cost):
    # init some values
    n_values = kwh_array.shape[0]
    max_storage = target_kw * n_values
    # add two values to array to represent previous and next years
    kwh_array = np.concatenate((
        np.array([max_storage + target_kw]),
        kwh_array,
        np.array([target_kw])
    ))
    # init array to keep track of storage at any given time
    storage_array = np.zeros(n_values + 1)
    # j is the index of a previous moment where there was a surplus
    j = 0
    # go through all values except the transition to next year
    for i in range(1, n_values + 1):
        # while there is a deficit at the current index i
        if kwh_array[i] > target_kw:
            j = i
            continue
        while kwh_array[i] < target_kw:
            # if previous index j has a surplus
            if kwh_array[j] > target_kw:
                amount = min(kwh_array[j] - target_kw, target_kw - kwh_array[i])
                # move kwh's from previous to current
                kwh_array[i] += amount
                kwh_array[j] -= amount
                # keep track of required storage
                storage_array[j:i] += amount
            else:
                # see if previous index has a surplus
                j -= 1

    # check transition to next year
    i = n_values + 1
    # make up for a possible deficit at the start of the year
    kwh_array[i] = kwh_array[0] - max_storage
    # j is the index of a previous moment where there was a surplus
    #j = i - 1
    while kwh_array[i] < target_kw:
        # if previous index j has a surplus
        if kwh_array[j] > target_kw:
            # move kwh's from previous to current
            kwh_array[i] += 1
            kwh_array[j] -= 1
            # keep track of required storage
            storage_array[j:i] += 1
        else:
            # see if previous index has a surplus
            j -= 1
            # if j reaches the position of the previous year,
            # not enough energy was produced this year
            if j == 0:
                break
    # calculate deficit
    deficit = target_kw - kwh_array[i]   
    # maximum storage required at any given point
    storage = np.amax(storage_array)
    # calculate the final cost
    cost = sp_sm * sp_cost_per_sm + \
        wm_m * wm_cost_per_m + \
        storage * st_cost_per_kwh +\
        deficit * deficit_cost
    return cost
"""
#@njit
def _calculate_cost_njit(kwh_array, sp_sm, wm_type,
        target_kw, sp_cost_per_sm, st_cost_per_kwh, deficit_cost):
    surplus_array = kwh_array - target_kw
    cumulative_array = np.cumsum(surplus_array)
    storage = 0
    deficit = min(0, cumulative_array[-1]) * -1
    if deficit == 0:
        smaller_than_zero = np.where(cumulative_array < 0)[0]
        if smaller_than_zero.shape[0] > 0:
            new_start = smaller_than_zero[-1] + 1
            surplus_array = np.concatenate((surplus_array[new_start:], surplus_array[:new_start]), axis=0)
            cumulative_array = np.cumsum(surplus_array)
        declining = surplus_array < 0
        while np.any(declining) and storage < np.max(cumulative_array):
            lowest = np.min(cumulative_array[declining])
            cumulative_array -= lowest
            new_start = np.where(np.logical_and(np.equal(cumulative_array, 0), declining))[0][-1] + 1
            storage = max(storage, np.max(cumulative_array[:new_start]))
            cumulative_array = cumulative_array[new_start:]
            declining = declining[new_start:]

    #windturbine shit
    if (wm_type == 2):
        wm_cost = 2
    elif (wm_type == 3):
        wm_cost = 3
    elif (wm_type == 1):
        wm_cost = 1
    else:
        wm_cost = 0
    # calculate the final cost
    cost = sp_sm * sp_cost_per_sm + \
        wm_cost + \
        storage * st_cost_per_kwh +\
        deficit * deficit_cost
    return cost

class CostCalculator():
    """
        class to calculaten the cost of a configuration
        sp_cost_per_sm = Solar panel cost per Square Meter
        wm_cost_per_m = Windmill cost per Meter
        st_cost_per_kwh = Storage Cost per KWH
    """

    def __init__(self, sp_cost_per_sm, st_cost_per_kwh, target_kw, deficit_cost):
        self.sp_cost_per_sm = sp_cost_per_sm
        self.st_cost_per_kwh = st_cost_per_kwh
        self.target_kw = target_kw
        self.deficit_cost = deficit_cost

    def calculate_cost(self, kwh_array, sp_sm, wm_type):
        # make a copy of the input array so we don't alter the original one
        kwh_array = copy(kwh_array)
        return _calculate_cost_njit(kwh_array, sp_sm, wm_type,
            self.target_kw, self.sp_cost_per_sm, self.st_cost_per_kwh, self.deficit_cost)
    
    def get_stats(self, kwh_array, sp_sm, wm_type):
        surplus_array = kwh_array - self.target_kw
        cumulative_array = np.cumsum(surplus_array)
        total_surplus = cumulative_array[-1]
        storage = 0
        deficit = min(0, total_surplus) * -1
        if deficit == 0:
            smaller_than_zero = np.where(cumulative_array < 0)[0]
            if smaller_than_zero.shape[0] > 0:
                new_start = smaller_than_zero[-1] + 1
                surplus_array = np.concatenate((surplus_array[new_start:], surplus_array[:new_start]), axis=0)
                cumulative_array = np.cumsum(surplus_array)
            declining = surplus_array < 0
            while np.any(declining) and storage < np.max(cumulative_array):
                lowest = np.min(cumulative_array[declining])
                cumulative_array -= lowest
                new_start = np.where(np.logical_and(np.equal(cumulative_array, 0), declining))[0][-1] + 1
                storage = max(storage, np.max(cumulative_array[:new_start]))
                cumulative_array = cumulative_array[new_start:]
                declining = declining[new_start:]
        #windturbine shit
        if (wm_type == 2):
            wm_cost = 2
        elif (wm_type == 3):
            wm_cost = 3
        elif (wm_type == 1):
            wm_cost = 1
        else:
            wm_cost = 0
        
        # calculate the final cost
        solar_cost = sp_sm * self.sp_cost_per_sm
        wind_cost = wm_cost
        storage_cost = storage * self.st_cost_per_kwh
        deficit_cost = deficit * self.deficit_cost
        cost = solar_cost + \
            wind_cost + \
            storage_cost +\
            deficit_cost
        stat_dict = {
            'cost': cost,
            'solar_cost': solar_cost,
            'wind_cost': wind_cost,
            'storage_cost': storage_cost,
            'deficit_cost': deficit_cost,
            'total_surplus': total_surplus,
            'total_storage': storage,
        }
        return stat_dict


# code example to test if storage and deficit calculations are working
if __name__ == '__main__':
    cost_calculator = CostCalculator(0, 1, 10, 100)
    print(0 == cost_calculator.calculate_cost(np.array([11, 11, 11, 10]), 0, 0))
    print(1 == cost_calculator.calculate_cost(np.array([11, 11, 11, 9]), 0, 0))
    print(2 == cost_calculator.calculate_cost(np.array([11, 11, 11, 8]), 0, 0))
    print(3 == cost_calculator.calculate_cost(np.array([11, 11, 11, 7]), 0, 0))
    print(100 == cost_calculator.calculate_cost(np.array([11, 11, 11, 6]), 0, 0))
    print(0 == cost_calculator.calculate_cost(np.array([10, 11, 11, 11]), 0, 0))
    print(1 == cost_calculator.calculate_cost(np.array([9, 11, 11, 11]), 0, 0))
    print(2 == cost_calculator.calculate_cost(np.array([8, 11, 11, 11]), 0, 0))
    print(3 == cost_calculator.calculate_cost(np.array([7, 11, 11, 11]), 0, 0))
    print(100 == cost_calculator.calculate_cost(np.array([6, 11, 11, 11]), 0, 0))
    print(2 == cost_calculator.calculate_cost(np.array([12, 8, 12, 8]), 0, 0))
    print(2 == cost_calculator.calculate_cost(np.array([8, 12, 8, 12]), 0, 0))
    print(6 == cost_calculator.calculate_cost(np.array([8, 16, 8, 8]), 0, 0))
