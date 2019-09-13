"""file containing class to run simulink from python"""

import numpy as np
import matlab.engine


class Simulink():
    """class to run simulink"""
    def __init__(self, model_name):
        self.model_name = model_name
        self.wind_model_name = model_name + '/Wind turbine'
        self.solar_model_name = model_name + '/Solar panels'
        self.engine = matlab.engine.start_matlab()
    
    def __del__(self):
        self.engine.quit()
    
    def run_simulation(self, solar_features, turbine_height):
        """run new simulation"""
        self.engine.Setup_parameters(nargout=0)
        self.engine.Setup_Toutdoor(nargout=0)
        self.engine.Setup_qsolar2(nargout=0)
        self.engine.Setup_wind(nargout=0)

        surface_features = solar_features[0::3]
        angle_features = solar_features[1::3]
        orientation_features = solar_features[2::3]

        azimuth = str(list(orientation_features)).replace(' ', '')
        inclanation = str(list(angle_features)).replace(' ', '')
        surface = str(list(surface_features)).replace(' ', '')
        efficiency = '[15]'

        power = '[0,0,10,80,160,300,400,400,400]'
        wind_velocity = '[0,1,2,4,6,8,10,20,30]'
        rotor_height =  str(turbine_height)  # '10'
        terrain_rating = '1'
        turbines = '0'

        self.engine.load_system(self.model_name)

        print(self.solar_model_name)
        print(azimuth)
        print(inclanation)
        print(surface)
        print(efficiency)

        self.engine.set_param(
            self.solar_model_name,
            'Az', azimuth,
            'Inc', inclanation,
            'Opp', surface,
            'ethasp', efficiency,
            nargout=0)

        self.engine.set_param(
            self.wind_model_name,
            'P', power,
            'v', wind_velocity,
            'h', rotor_height,
            'a', terrain_rating,
            'nwt', turbines,
            nargout=0)
        
        output = self.engine.sim(self.model_name, 'ReturnWorkspaceOutputs', 'on')
        self.engine.workspace['Output'] = output
        output = np.array(self.engine.eval("Output.Ptotal"))
        total = np.sum(output[:,1:], axis=1)
        return total

if __name__ == '__main__':
    sim = Simulink('WT_SP_model_vs1total')

    output = sim.run_simulation(np.array([1000, 15, 0, 0, 15, 0, 0, 45, 0, 0, 0, 0]), 10)

    print(output)
    print(np.mean(output))
