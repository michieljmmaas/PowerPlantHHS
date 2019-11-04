"""train a single group"""

import numpy as np
import pandas as pd
from calculate_cost import CostCalculator
from genetic_algorith import GeneticAlgorith
from run_sim import Simulink
from save_and_load import PopulationSaver

N_PANELS = 4
N_SOLAR_FEATURES = N_PANELS * 3
N_WIND_FEATURES = 1
N_WIND_MAX = 20
N_FEATURES = N_SOLAR_FEATURES + N_WIND_FEATURES


def train(n_generations, group_size, surface_min, surface_max, angle_min, angle_max,
          orientation_min, orientation_max, model_name=None, load=False):
    """train genetic algorithm"""

    genetic_algorithm = GeneticAlgorith(50, 100, 6, 2, 2, True)
    cb_cost_table = pd.DataFrame({'area':[1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 600, 1000, 1250, 1600, 2000, 3000, 5000, 8000 , 10000, 12000, 15000, 18000, 22000, 25000, 30000, 40000, 50000],
        'cost':[0.002, 0.003, 0.008, 0.013, 0.014, 0.016, 0.025, 0.035, 0.075, 0.1, 0.15, 0.22, 0.3, 0.39, 0.49, 0.5, 0.62, 0.8, 1.25, 1.6, 2, 2.5, 3.5, 6, 9, 11, 13, 17.5, 20, 30, 40, 50, 60, 72]})
    # parameter 2 kosten voor accu per kWh
    cost_calculator = CostCalculator(190, 400, 6000, 1000000, cb_cost_table, 1000, 230)
    simulink = Simulink('WT_SP_model_vs1total')
    saver = PopulationSaver(model_name, load)

    if load:
        group_values = saver.load()
    else:
        # generate random values in valid range
        solar_values = np.random.rand(group_size, N_SOLAR_FEATURES)
        solar_values[:, 0::3] *= (surface_max - surface_min)
        solar_values[:, 0::3] += surface_min
        solar_values[:, 1::3] *= (angle_max - angle_min)
        solar_values[:, 1::3] += angle_min
        solar_values[:, 2::3] *= (orientation_max - orientation_min)
        solar_values[:, 2::3] += orientation_min
        wind_values = np.random.rand(group_size, N_WIND_FEATURES)
        wind_values *= N_WIND_MAX
        group_values = np.concatenate((solar_values, wind_values), axis=1)  # concatenate on features
        

    # prepare min and max arrays to truncate values later
    highest_allowed = np.zeros_like(group_values)
    lowest_allowed = np.zeros_like(group_values)
    highest_allowed[:, 0:N_SOLAR_FEATURES:3] = surface_max
    lowest_allowed[:, 0:N_SOLAR_FEATURES:3] = surface_min
    highest_allowed[:, 1:N_SOLAR_FEATURES:3] = angle_max
    lowest_allowed[:, 1:N_SOLAR_FEATURES:3] = angle_min
    highest_allowed[:, 2:N_SOLAR_FEATURES:3] = orientation_max
    lowest_allowed[:, 2:N_SOLAR_FEATURES:3] = orientation_min
    highest_allowed[:, -1] = N_WIND_MAX
    lowest_allowed[:, -1] = 0
        

    last_generation = n_generations - 1
    for generation in range(saver.generation, n_generations):
        cost_array = np.zeros(group_size)
        print('finished simulation 0 of {}'.format(group_size), end='\r')
        for i in range(group_size):
            current_row = group_values[i]
            # selecting windturbine type
            wm_type = 4
            n_Turbines = int(current_row[-1])
            # run simulink
            energy_production, _ = simulink.run_simulation(current_row[:N_SOLAR_FEATURES], wm_type, n_Turbines)  # add turbine later
            #energy_production = np.array([np.sum(current_row[:N_SOLAR_FEATURES:3])] * (365*24))  # simple fake simulation
            # run cost calculator
            sp_sm = np.sum(current_row[0:N_SOLAR_FEATURES:3])
            cost_array[i] = cost_calculator.calculate_cost(energy_production, sp_sm, wm_type, n_Turbines)  # add turbine later
            # print progress
            print('finished simulation {} of {}'.format(i+1, group_size), end='\r')
        # log and print progress
        saver.log(
            'generation:', saver.generation,
            'mean_cost:', np.mean(cost_array),
            'min_cost:', np.min(cost_array),
            to_screen=True)
        # store intermediate result
        best = genetic_algorithm.get_best(group_values, cost_array)
        saver.save_best(best)
        # quit when done
        if generation == last_generation:
            return best
        # run genetic algorithm
        group_values = genetic_algorithm.generate_new_population(group_values, cost_array)
        # remove illegal values
        group_values = np.minimum(group_values, highest_allowed)
        group_values = np.maximum(group_values, lowest_allowed)
        # store intermediate population
        saver.save(group_values)


if __name__ == '__main__':
    train(10000, 100, 0, 10000000, 0, 90, 0, 359, model_name= '20191031_111207', load=True)
