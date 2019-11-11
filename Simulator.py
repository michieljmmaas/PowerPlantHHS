import numpy as np
import pandas as pd
from datetime import datetime
from generators import Windturbine
#from location import Location
import time
import warnings
warnings.filterwarnings("ignore")

KAPPA = 1.041  # for calculations in radians
IO = 1366.1  # solar constant(w/m^2)
NANO = 1e-9  # for conversion from nanoseconds
LSM = 15  # local standard time meridian


class Simulator():
    """Class for calculating irradiation"""

    def __init__(self, file_name, sheet_name, Windturbine, skiprows=None, index_col=None, latitude=51.95,
                 longitude=4.45, lsm=15, terrain_factor=0.19):
        # variables from arguments
        self.latitude = latitude
        self.longitude = longitude
        self.terrain_factor = terrain_factor
        self.Windturbine = Windturbine

        # variables from data file
        self.import_data = pd.read_excel(file_name, sheet_name, skiprows=skiprows, index_col=index_col)
        self.ghi = self.import_data.iloc[:, 4].values
        self.dni = self.import_data.iloc[:, 7].values
        self.dates = self.import_data.iloc[:, 18].values
        # self.doy = np.array([datetime.utcfromtimestamp(self.dates[i].astype(int) * NANO).timetuple().tm_yday for i in range(0,len(self.dates))])
        self.doy = self.dates
        self.time = self.import_data.iloc[:, 3].values
        self.wind_speed = self.import_data.iloc[:, 20].values
        self.temperature = self.import_data.iloc[:, 19].values

    def calc_solar(self, Az=[0, 0, 0, 0], Inc=[15, 15, 15, 15], sp_area=[100, 100, 100, 100], sp_eff=16, gref=0):
        gamma = np.array(Az)
        beta = np.array(Inc)

        # calculation of sun positions                         
        day_angle = 2 * np.pi * (self.doy - 1) / 365
        decl = 23.442 * np.sin(np.deg2rad((360 / 365) * (self.doy + 284)))

        # equation of time 
        EQT = 229.18 * (0.0000075 + 0.001868 * np.cos(np.deg2rad(day_angle))
                        - 0.032077 * np.sin(np.deg2rad(day_angle)) - 0.014615 * np.cos(np.deg2rad(2 * day_angle))
                        - 0.040849 * np.sin(np.deg2rad(2 * day_angle)))

        # hour angle [deg] 
        h = 15 * ((self.longitude - LSM) * 4 / 60 + (self.time - 12 - 0.5 + EQT / 60))
        hai = np.round(np.sin(np.deg2rad(self.latitude)), 4) * np.round(np.sin(np.deg2rad(decl)), 4) + np.round(
            np.cos(np.deg2rad(self.latitude)), 4) * np.round(np.cos(np.deg2rad(decl)) * np.cos(np.deg2rad(h)), 4)

        # calculating DHI from GHI and DNI
        DHI = self.ghi - self.dni * hai
        DHI[DHI < 0] = 0

        sel = np.degrees(np.arcsin(hai))  # sel=solar elevation angle [deg]
        Zen = np.arccos(hai)  # Zen=solar zenith angle [radians!!]

        # Perez factors for calculation of circumsolar and horizon brightness coefficients
        f11 = np.array([-0.008, 0.130, 0.330, 0.568, 0.873, 1.132, 1.060, 0.678])
        f12 = np.array([0.588, 0.683, 0.487, 0.187, -0.392, -1.237, -1.600, -0.327])
        f13 = np.array([-0.062, -0.151, -0.221, -0.295, -0.362, -0.412, -0.3590, -0.2500])
        f21 = np.array([-0.0600, -0.0190, 0.0550, 0.1090, 0.2260, 0.2880, 0.2640, 0.1560])
        f22 = np.array([0.072, 0.066, -0.064, -0.152, -0.462, -0.823, -1.1270, -1.3770])
        f23 = np.array([-0.022, -0.029, -0.026, -0.014, 0.001, 0.056, 0.131, 0.2510])

        # determination of bin with eps
        s_bin = np.ones(len(self.time))  # bin 1 is overcast sky , bin 8 is clear sky
        eps = ((DHI + self.dni) / DHI + KAPPA * Zen ** 3) / (1 + KAPPA * Zen ** 3)

        s_bin[np.logical_and(eps >= 1.065, eps < 1.23)] = 2
        s_bin[np.logical_and(eps >= 1.23, eps < 1.5)] = 3
        s_bin[np.logical_and(eps >= 1.5, eps < 1.95)] = 4
        s_bin[np.logical_and(eps >= 1.95, eps < 2.8)] = 5
        s_bin[np.logical_and(eps >= 2.8, eps < 4.5)] = 6
        s_bin[np.logical_and(eps >= 4.5, eps < 6.2)] = 7
        s_bin[(eps >= 6.2)] = 8

        # calculation of relative air mass
        M = 1 / hai
        M[sel < 2] = 20

        ETR = IO * (1 + 0.033 * np.cos(np.deg2rad(2 * np.pi * self.doy)) / 365)  # [deg]

        Delta = (DHI * M) / ETR

        s_bin_int = s_bin.astype(int)

        F1 = f11[s_bin_int - 1] + Delta * f12[s_bin_int - 1] + Zen * f13[s_bin_int - 1]
        F1[F1 < 0] = 0
        F2 = f21[s_bin_int - 1] + Delta * f22[s_bin_int - 1] + Zen * f23[s_bin_int - 1]

        # determination of cos angle of incidence of tilted surface 
        #  cai= cos angle of incidence of Solar to surface = cos(teta)
        gamma_dim = gamma[np.newaxis, :]
        beta_dim = beta[np.newaxis, :]
        decl_dim = decl[:, np.newaxis]
        h_dim = h[:, np.newaxis]

        cai = np.array(np.sin(np.deg2rad(decl_dim)) * np.sin(np.deg2rad(self.latitude)) * np.cos(np.deg2rad(beta_dim))
                       - np.sin(np.deg2rad(decl_dim)) * np.cos(np.deg2rad(self.latitude)) * (
                                   np.sin(np.deg2rad(beta_dim)) * np.cos(np.deg2rad(gamma_dim)))
                       + (np.cos(np.deg2rad(decl_dim)) * np.cos(np.deg2rad(h_dim))) * np.cos(
            np.deg2rad(self.latitude)) * np.cos(np.deg2rad(beta_dim))
                       + (np.cos(np.deg2rad(decl_dim)) * np.cos(np.deg2rad(h_dim))) * np.sin(
            np.deg2rad(self.latitude)) * (np.sin(np.deg2rad(beta_dim)) * np.cos(np.deg2rad(gamma_dim)))
                       + np.cos(np.deg2rad(decl_dim)) * np.sin(np.deg2rad(h_dim)) * (
                                   np.sin(np.deg2rad(beta_dim)) * np.sin(np.deg2rad(gamma_dim))))

        # determination of the diffuse radiation on a tilted surface DTI, Perez 1990
        a = cai
        a[a < 0] = 0

        b = np.cos(Zen)
        b[b < 0.087] = 0.087

        # Adjust for broadcast operations
        b = b[:, np.newaxis]
        DHI_dim = DHI[:, np.newaxis]
        F1_dim = F1[:, np.newaxis]
        F2_dim = F2[:, np.newaxis]
        DNI_dim = self.dni[:, np.newaxis]

        c = (a / b) * F1_dim

        DTI = DHI_dim * (1 - F1_dim) * (1 + np.cos(np.deg2rad(beta_dim))) / 2 + c + F2_dim * np.sin(
            np.deg2rad(beta_dim))
        DTI[DTI < 0] = 0

        DSTI = cai * DNI_dim
        DSTI[DSTI < 0] = 0

        Rg = 0.5 * gref * (DHI_dim + DNI_dim) * (1 - np.cos(np.deg2rad(beta_dim)))

        GTI = DTI + DSTI + Rg

        individual_output = (GTI * (sp_eff / 100)) * sp_area

        total_output = np.sum(individual_output, axis=1)

        P_out = total_output / 1000  # kW

        """        
        Solar calculations according to Matlab script
        E = total_output/(3600)*10^-6

        for some reason matlab does not devide by 3600 resulting in the calculation
        having the same outcome as the one below

        """
        E_out = np.cumsum(total_output / 1000000)

        return P_out, E_out

    def calc_wind(self, n_turbines):
        external_factors = (self.Windturbine.rotor_height / 10) ** self.terrain_factor

        in_values = self.wind_speed * external_factors

        excl = self.Windturbine.wind_curve[np.newaxis, :] - in_values[:, np.newaxis]
        abs_excl = np.abs(excl)

        index_1 = abs_excl.argmin(axis=1)
        index_2 = index_1 - 1
        index_2[excl[np.arange(in_values.shape[0]), index_1] < 0] += 2

        a_1 = self.Windturbine.wind_curve[index_1]
        a_2 = self.Windturbine.wind_curve[index_2]

        difference_1 = np.abs(a_1 - in_values)
        difference_2 = np.abs(a_2 - in_values)
        difference = difference_1 + difference_2

        value_1 = self.Windturbine.power_curve[index_1]
        value_2 = self.Windturbine.power_curve[index_2]

        P_out_single = (value_1 * difference_2 + value_2 * difference_1) / difference  # kW
        P_out = P_out_single * n_turbines  # kW

        E_out = np.cumsum(P_out / 1000)  # MWh

        return P_out, E_out

    def calc_total_power(self, solar_features, wind_features, sp_eff):
        surface_features = solar_features[0::3]
        angle_features = solar_features[1::3]
        orientation_features = solar_features[2::3]


        self.terrain_factor = wind_features[1]
        wind,_ = self.calc_wind(wind_features[0])
        solar,_ =self.calc_solar(Az=orientation_features, Inc=angle_features, sp_area=surface_features, sp_eff=sp_eff)

        total_power = wind + solar

        return total_power, [wind.tolist(), solar.tolist()]


if __name__ == '__main__':
    file = 'formatted_data.xls'
    sheet = '1%overschrijding-B.2'

    start_time = time.time()

    turbine = Windturbine(4)

    sim = Simulator(file, sheet, turbine, skiprows=[0, 1, 2, 3])

    p_wind, e_wind = sim.calc_wind(7)
    p_solar, e_solar = sim.calc_solar(Az=[0, 0, 0, 0], Inc=[15, 15, 15, 15], sp_area=[100, 100, 100, 100])

    df = pd.DataFrame({'p_wind': p_wind, 'e_wind': e_wind, 'p_solar': p_solar, 'e_solar': e_solar})
    df.index = df.index + 1

    #df.to_excel('Simulator_out.xlsx')

    end_time = time.time()

    duration = end_time - start_time

    print('Time elapsed: ' + str(duration))

