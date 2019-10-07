import numpy as np
from run_sim import Simulink

if __name__ == '__main__':
    surface_var = 1000

    sim = Simulink('WT_SP_model_vs1total')
    _,output = sim.run_simulation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],0,0)
    solar_output = output[:, 2]

    with open('testfile.csv', 'w') as file:
        row = ','.join(['Angle', 'Orientation', 'Ptotal'] + [str(i) for i in range(0,solar_output.shape[0])])
        print(row, file=file)
        for ang_it in range(0, 90, 1):
            for or_it in range(0, 360, 5):
                _,output = sim.run_simulation([surface_var, ang_it, or_it, 0, 0, 0, 0, 0, 0, 0, 0, 0],0,0)
                solar_output = output[:, 2]
                row = ','.join([str(s) for s in ([ang_it, or_it, np.sum(solar_output)] + list(solar_output))])
                print(row, file=file)
                print(ang_it, or_it)
