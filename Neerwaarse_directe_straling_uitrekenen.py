"""Berekent de neerwaarse directe zonnestraling uit vanuit de globale straling"""

import numpy as np


AIRPRESSURE = 1013.25
SOLAIRPRODUCTION = 1370

def globle_to_direct(
        latitude,
        longtitude,
        time_zone,
        doy,
        hour,
        pressure,
        global_radiation,
        ):
    day_angle = 6.283185 * (doy-1) / 365
    ETR = SOLAIRPRODUCTION * (1.00011 + 0.034221 * np.cos(day_angle) + 0.00128 * np.sin(day_angle) + 0.000719 * np.cos(2 * day_angle) + 0.000077 * np.sin(2 * day_angle))
    
    DEC = (0.006918 - 0.399912 * np.cos(day_angle) + 0.070257 * np.sin(day_angle) - 0.006758 * np.cos(2*day_angle) + 0.000907 * np.sin(2 * day_angle) - 0.002697 * np.cos(3 * day_angle) + 0.00148 * np.sin(3 * day_angle)) * (180/np.pi)
    EQT = (0.000075 + 0.001868 * np.cos(day_angle) - 0.032077 * np.sin(day_angle) - 0.014615 * np.cos(2*day_angle) - 0.040849 * np.sin(2 * day_angle)) * (229.18)
    hour_angle = 15 * (hour - 12 - 0.5 + EQT / 60 + ((longtitude-time_zone * 15) * 4) / 60)
    zenith_angle = np.arccos(np.cos(np.radians(DEC)) * np.cos(np.radians(latitude)) * np.cos(np.radians(hour_angle)) + np.sin(np.radians(DEC)) * np.sin(np.radians(latitude))) * (180/np.pi)
    pressure_condision_of_air_mass = pressure/AIRPRESSURE
    
    am = np.zeros_like(zenith_angle)
    zenith_angle_lt_80 = zenith_angle < 80
    
    am[zenith_angle_lt_80] = (1 / (np.cos(np.radians(zenith_angle[zenith_angle_lt_80])) + 0.15 / (93.885 - zenith_angle[zenith_angle_lt_80]) ** 1.253)) * pressure_condision_of_air_mass[zenith_angle_lt_80]
    
    # kt
    kt = np.zeros_like(am)
    am_gt_0 = am > 0
    kt[am_gt_0] = global_radiation[am_gt_0]/(np.cos(np.radians(zenith_angle[am_gt_0])) * ETR[am_gt_0])
    
    kt_gt_0 = kt > 0
    kt_gt_06 = kt > 0.6
    kt_lte_06 = kt <= 0.6
    kt_gt_0_lte_06 = kt_gt_0 & kt_lte_06

    kt_where_kt_gt_06 = kt[kt_gt_06]
    kt_where_kt_gt_0_lte_06 = kt[kt_gt_0_lte_06]

    # A
    a = np.zeros_like(am)
    a[kt_gt_06] = -5.743 + 21.77 * kt_where_kt_gt_06 - 27.49 * kt_where_kt_gt_06 ** 2 + 11.56 * kt_where_kt_gt_06 ** 3
    a[kt_gt_0_lte_06] = 0.512 - 1.56 * kt_where_kt_gt_0_lte_06 + 2.286 * kt_where_kt_gt_0_lte_06 ** 2 - 2.222 * kt_where_kt_gt_0_lte_06 ** 3
    

    # B
    b = np.zeros_like(am)   
    b[kt_gt_06] = 41.4 - 118.5 * kt_where_kt_gt_06 + 66.05 * kt_where_kt_gt_06 ** 2 + 31.9 * kt_where_kt_gt_06 ** 3
    b[kt_gt_0_lte_06] = 0.37 + 0.962 * kt_where_kt_gt_0_lte_06 


    
    # C
    c = np.zeros_like(am)
    c[kt_gt_06] =  -47.01 + 184.2 * kt_where_kt_gt_06 - 222 * kt_where_kt_gt_06 ** 2 + 73.81 * kt_where_kt_gt_06 ** 3
    c[kt_gt_0_lte_06] = -0.28 + 0.932 * kt_where_kt_gt_0_lte_06 - 2.048 * kt_where_kt_gt_0_lte_06 ** 2

    
    # deltakn
    am_where_kt_gt_0 = am[kt_gt_0]
    deltakn = np.zeros_like(am)
    deltakn[kt_gt_0] = a[kt_gt_0] + b[kt_gt_0] * np.exp((c[kt_gt_0] * am_where_kt_gt_0))

    
    # knc
    knc = np.zeros_like(am)
    knc[kt_gt_0] = 0.886 - 0.122 * am_where_kt_gt_0 + 0.0121 * am_where_kt_gt_0 ** 2 - 0.000653 * am_where_kt_gt_0 ** 3 + 0.000014 * am_where_kt_gt_0 ** 4


    # DNI
    DNI = np.zeros_like(am)
    DNI[kt_gt_0] = ETR[kt_gt_0] * (knc[kt_gt_0] - deltakn[kt_gt_0])
    

    return DNI

    


