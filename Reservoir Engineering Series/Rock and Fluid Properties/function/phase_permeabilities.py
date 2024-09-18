import pandas as pd

def calculate(dataframe: pd.DataFrame, mu_oil, mu_water, core_length, dP, core_area) -> pd.DataFrame:
    """
    Calculate Phase permeabilities for oil and water
    by Pandu Hafizh Ananta

    Parameters:
    dataframe (pd.DataFrame): DataFrame Containing 'qo' (Oil flowrate), 'qw' (Water Flowrate), and 'Sw' (Water saturation)
    mu_oil : Oil Viscosity, given by float number, units (cP)
    mu_water : Water Viscosity, given by float number, units (cP)
    core_length : Cylindrical core dimension length, given by float number, units (cm)
    dP : Pressure drop, given by float number, units (atm)
    core_area : core dimension flow area, given by float, units (cm^2)
    """
    dataframe['k_o'] = (dataframe['qo'] * mu_oil / core_area) / (dP/core_length)
    dataframe['k_w'] = (dataframe['qw'] * mu_water / core_area) / (dP/core_length)

    return dataframe
