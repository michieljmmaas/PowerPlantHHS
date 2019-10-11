"""file containing class to run simulink from python"""

import numpy as np
import matlab.engine
from windTurbine import WindTurbine


class Simulink():
    """class to run simulink"""
    def __init__(self, model_name, efficiency='[15]', terrain_rating='0.12'):
        self.model_name = model_name
        self.wind_model_name = model_name + '/Wind turbine'
        self.solar_model_name = model_name + '/Solar panels'
        self.engine = matlab.engine.start_matlab()
        self.engine.warning('off', nargout=0)
        self.efficiency = efficiency
        self.terrain_rating = terrain_rating
    
    def __del__(self):
        self.engine.quit()
    
    def run_simulation(self, solar_features, wm_type, n_Turbine):
        """run new simulation"""
        self.engine.Setup_parameters(nargout=0)

        surface_features = solar_features[0::3]
        angle_features = solar_features[1::3]
        orientation_features = solar_features[2::3]

        azimuth = str(list(orientation_features)).replace(' ', '')
        inclanation = str(list(angle_features)).replace(' ', '')
        surface = str(list(surface_features)).replace(' ', '')

        windTurbine = WindTurbine(n_turbines=str(n_Turbine), wm_type=wm_type)

        self.engine.load_system(self.model_name)

        self.engine.set_param(
            self.solar_model_name,
            'Az', azimuth,
            'Inc', inclanation,
            'Opp', surface,
            'ethasp', self.efficiency,
            nargout=0)

        self.engine.set_param(
            self.wind_model_name,
            'P', windTurbine.power,
            'v', windTurbine.wind_velocity,
            'h', windTurbine.rotor_height,
            'a', self.terrain_rating,
            'nwt', windTurbine.n_turbines,
            nargout=0)

        self.engine.Setup_Toutdoor(nargout=0)
        self.engine.Setup_qsolar2(nargout=0)
        self.engine.Setup_wind(nargout=0)        
        
        output = self.engine.sim(self.model_name, 'ReturnWorkspaceOutputs', 'on')
        self.engine.workspace['Output'] = output
        output = np.array(self.engine.eval("Output.Ptotal"))
        total = np.sum(output[:, 1:], axis=1)
        return total, output

if __name__ == '__main__':
    sim = Simulink('WT_SP_model_vs1total')
    output, all_out = sim.run_simulation(np.array([1000, 15, 0, 1000, 15, 0, 1000, 15, 0, 1000, 15, 0]), 4, 7)

    print('Total: ' + str(np.sum(output)))
    print('Mean: ' + str(np.mean(output)))

