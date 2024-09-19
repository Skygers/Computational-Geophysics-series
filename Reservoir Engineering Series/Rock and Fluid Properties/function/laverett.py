import pandas as pd
import numpy as np

def Jfunction(dataframe: pd.DataFrame, sigma, theta, k: list, poro: list) -> pd.DataFrame:
    '''
    Laverett J Function parentheses using dataframe pandas framework
    this function only works with data contains 4 cores, if you have more or less than 4 cores, change the variable function below
    \nby Pandu Hafizh Ananta

    Parameter:
    dataframe: Table contains measured four cores or more, flexible but changes function below in necessary\n
    sigma: The oil/water interfacial tension (dynes/cm, psi/cm, ect), the relevant factors or untis are necessary\n
    theta: Angle of wettabiity (deg)\n
    k: list of permeabilities of oil/water corresponding to every cores, relevant factors or units are necessary\n
    poro: list of porosity of oil/water corresponding to every cores\n
    '''

    dataframe['J_1'] = (dataframe['pc_1'] / (sigma * np.cos(np.deg2rad(theta)))) * np.sqrt(k[0]/poro[0])
    dataframe['J_2'] = (dataframe['pc_2'] / (sigma * np.cos(np.deg2rad(theta)))) * np.sqrt(k[1]/poro[1])
    dataframe['J_3'] = (dataframe['pc_3'] / (sigma * np.cos(np.deg2rad(theta)))) * np.sqrt(k[2]/poro[2])
    dataframe['J_4'] = (dataframe['pc_4'] / (sigma * np.cos(np.deg2rad(theta)))) * np.sqrt(k[3]/poro[3])
    return dataframe
