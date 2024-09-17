"""
Fluid Property Modelling with Batzle-Wang (1991) for brine and gas
by Pandu Hafizh Ananta
"""

import numpy as np

# Batzle-Wang for brine

def BW_brine_density(temp, Pp_baseline, salinity):
    rhow = 1 + (0.000001) * (
        (-80 * temp) - (3.3 * (temp**2)) + (0.00175 * (temp**3)) + (489 * Pp_baseline) - (2 * temp * Pp_baseline)
        + (0.016 * (temp**2) * Pp_baseline) - (0.000013 * (temp**3) * Pp_baseline)
        - (0.333 * (Pp_baseline**2)) + (0.002 * temp * (Pp_baseline**2))
    )

    rhobrine = rhow + (0.668 * salinity) + (0.44 * salinity**2) + (
        1e-5 * salinity * (
            (300 * Pp_baseline) - (2400 * Pp_baseline * salinity) + temp * (
                80 + (3 * temp) - (3300 * salinity) - (13 * Pp_baseline) + (47 * Pp_baseline * salinity)
            )
        )
    )
    
    return rhobrine

def BW_brine_bulk(temp, Pp_baseline, salinity, rhobrine):
    # Pre-calculating powers of temperature and pressure
    temp_powers = [temp**i for i in range(5)]
    Pp_powers = [Pp_baseline**i for i in range(4)]

    vw_coeffs = [
        1402.85, 4.871, -0.04783, 1.487E-04, -2.197E-07,
        1.524, -0.0111, 2.747E-04, -6.503E-07, 7.987E-10,
        3.437E-03, 1.739E-04, -2.135E-06, -1.455E-08, 5.23E-11,
        -1.197E-05, -1.628E-06, 1.237E-08, 1.327E-10, -4.614E-13
    ]
    
    vw = [vw_coeffs[i] * temp_powers[i % 5] * Pp_powers[i // 5] for i in range(20)]
    vwsum = sum(vw)
    
    vbrine = vwsum + (salinity * (1170 - (9.6 * temp) + (0.055 * temp**2) - (8.5E-05 * temp**3)
              + (2.6 * Pp_baseline) - (0.0029 * temp * Pp_baseline) - (0.0476 * Pp_baseline**2))) \
              + (salinity**1.5 * (780 - (10 * Pp_baseline) + (0.16 * Pp_baseline**2))) \
              - (1820 * salinity**2)

    Kbrine = rhobrine * vbrine**2 * 1e-6  # in GPa
    return Kbrine

# Batzle-Wang for gas

def BW_gas_density(temp, SG, Pp_post):
    R = 8.314472  # gas constant
    temp_abs = temp + 273.15  # Kelvin
    P_pr = Pp_post / (4.892 - (0.40486 * SG))
    T_pr = temp_abs / (94.72 + (170.75 * SG))
    E = 0.109 * ((3.85 - T_pr)**2) * np.exp(-0.45 - 8 * (0.56 - 1 / T_pr)**2 * (P_pr**1.2) / T_pr)
    Z = (0.03 + 0.00527 * (3.5 - T_pr)**3) * P_pr + (0.642 * T_pr - 0.007 * T_pr**4 - 0.52) + E
    rhogas = (28.8 * SG * Pp_post) / (Z * R * temp_abs)
    return rhogas

def BW_gas_bulk(temp, SG, Pp_post):
    temp_abs = temp + 273.15  # Kelvin
    P_pr = Pp_post / (4.892 - (0.40486 * SG))
    T_pr = temp_abs / (94.72 + (170.75 * SG))
    E = 0.109 * ((3.85 - T_pr)**2) * np.exp(-0.45 - 8 * (0.56 - 1 / T_pr)**2 * (P_pr**1.2) / T_pr)
    Z = (0.03 + 0.00527 * (3.5 - T_pr)**3) * P_pr + (0.642 * T_pr - 0.007 * T_pr**4 - 0.52) + E
    
    Gamma0 = 0.85 + 5.6 / (P_pr + 2) + 27.1 / (P_pr + 3.5)**2 - 8.7 * np.exp(-0.65 * (P_pr + 1))
    F = -1.2 * (P_pr**0.2 / T_pr) * (0.45 + 8 * (0.56 - 1 / T_pr)**2) * np.exp(-0.45 - 8 * (0.56 - 1 / T_pr)**2 * (P_pr**1.2 / T_pr))
    doZ_doPpr = 0.03 + 0.00527 * (3.5 - T_pr)**3 + 0.109 * (3.85 - T_pr)**2 * F

    Kgas = Pp_post * Gamma0 / (1 - (P_pr / Z * doZ_doPpr))
    return Kgas
