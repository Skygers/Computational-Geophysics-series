import pandas as pd


def calculate(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate relative permeabilities for oil and water.
    by Pandu Hafizh Ananta

    Parameters:
    dataframe (pd.DataFrame): DataFrame containing 'qo' (oil flowrate), 'qw' (water flowrate), and 'Sw' (water saturation).

    Returns:
    pd.DataFrame: DataFrame with additional columns for 'kr_o' and 'kr_w' (relative permeabilities).
    """
    dataframe['kr_o'] = dataframe['qo'] / dataframe['qo'].iloc[0]  # Relative permeability of oil
    dataframe['kr_w'] = dataframe['qw'] / dataframe['qw'].iloc[-1] # Relative permeability of water
    return dataframe