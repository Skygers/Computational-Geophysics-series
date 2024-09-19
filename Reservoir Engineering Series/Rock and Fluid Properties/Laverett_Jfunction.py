import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("Reservoir Engineering Series")
import utilities
from function import laverett
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

'''
Calculation of the Laverett J Function
by Pandu Hafizh Ananta

given table or data with filename "Table 1.1 Capillary Pressure Sets Example.csv"
this table was measured for four cores from the same reservoir

Parameter
sigma: the oil/water interfacial tension, value = 72 dynes/cm
theta: angle of wettability, value = 45 deg
'''

#importing table or dataset of capillary pressure sets
df = pd.read_csv("Reservoir Engineering Series\Rock and Fluid Properties\data\Table 1.1 Capillary Pressure Sets Example.csv")

#declare parameters for calculation purpose
sigma = 72 #dynes/cm (need to convert to psi/cm)
theta = 45 #deg (in calculation this value convert in radian)
poro = [0.08, 0.11, 0.15, 0.22] #porosity every cores, shows in table
k = [1.0, 15.0, 100.0, 500.0] #md (need to convert to cm)
k_convert = []

#converting sigma
sigma_converted = utilities.dyne_cm_to_psi_cm(sigma)

#converting permeabilities first
for i in k:
    convert = utilities.milidarcy_to_micro_m2(i) * 1E-8
    k_convert.append(convert)

#calculated J Function
calculated  = laverett.Jfunction(dataframe=df, sigma=sigma_converted, theta=theta, k=k_convert, poro=poro)
print("calculating J funtion is done..\n")
print("showing table after calculation\n", calculated)


#plotting laveret function results
plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots(1, figsize=(10,5), dpi=100)
ax.plot(calculated["sw"], calculated["J_1"], label=r'Laverett J Function 1', linewidth=2, color='blue')
ax.plot(calculated["sw"], calculated["J_2"], label=r'Laverett J Function 2', linewidth=2, color='green')
ax.plot(calculated["sw"], calculated["J_3"], label=r'Laverett J Function 3', linewidth=2, color='red')
ax.plot(calculated["sw"], calculated["J_4"], label=r'Laverett J Function 4', linewidth=2, color='black')

ax.set_xlabel(r'$S_W$ (%)', fontsize=14)
ax.set_ylabel(r'$J_{function}$', fontsize=14)
ax.grid(True, which='both', linestyle='--', linewidth=0.6)
ax.legend(fontsize=12, loc='best')
ax.set_title("The Laverett J Function Curves")

fig.tight_layout()
fig.savefig("Reservoir Engineering Series\Rock and Fluid Properties\output\Laverett J Function Curves.png", dpi=100)

plt.show()