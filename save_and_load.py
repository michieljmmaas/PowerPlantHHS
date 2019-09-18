"""save and load checkpoints and log progress"""

import os
import numpy as np
import datetime


class PopulationSaver():
    """object to save and load checkpoints and write logs"""
    def __init__(self, model_name=None, load=False):
        self.generation = 0

        if model_name is None:
            model_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.path = 'saved_runs\\' + model_name

        if not os.path.isdir('saved_runs'):
            os.mkdir('saved_runs')
        if os.path.isdir(self.path):
            if load == False:
                raise Exception('model already exists')
        elif load == True:
            raise Exception('model doesn\'t exists')
        else:
            os.mkdir(self.path)
        
        self.path += '\\'
        self.log_file = self.path + 'log.txt'

        if load:
            highest = 0
            for file_name in os.listdir(self.path):
                split = file_name.split('_')
                if len(split) == 2 and split[0] == 'generation':
                    highest = max(int(split[1].split('.')[0]), highest)
            self.generation = highest
    
    def log(self, *args, to_screen=False):
        with open(self.log_file, mode='a') as log_file:
            print(*args, file=log_file)
        if to_screen:
            print(*args)
    
    def save(self, array):
        """save an array with population"""
        np.savetxt(self.path + 'generation_' + str(self.generation) + '.csv', array, delimiter=',')
        self.generation += 1
    
    def save_best(self, array):
        """save an array with best picks"""
        np.savetxt(self.path + 'best_' + str(self.generation) + '.csv', array, delimiter=',')
    
    def load(self, generation=None):
        """load an array"""
        if generation is None:
            generation = self.generation
        elif generation < 0:
            generation = self.generation - generation
        return np.loadtxt(self.path + 'generation_' + str(generation) + '.csv', delimiter=',')


if __name__ == '__main__':
    population_saver = PopulationSaver()
    population_saver.log('created')
    a = np.array([[1, 2], [3, 4], [5, 6]])
    population_saver.save(a)
    population_saver.log('stored a with average value', np.mean(a))
    b = a * 2
    population_saver.save(b)
    population_saver.log('stored b with average value', np.mean(b))
    c = population_saver.load()
    population_saver.log('loaded b into c')
    population_saver.log('b == c', b == c)
    population_saver.save_best(c)
    population_saver.log('stored c as best')
