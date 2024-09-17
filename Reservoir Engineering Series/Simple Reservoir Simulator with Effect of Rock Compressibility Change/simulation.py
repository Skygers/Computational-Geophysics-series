"""
Simple Reservoir Simulator with Effect of Rock Compressibility Change
By: Pandu Hafizh Ananta
"""

import matplotlib.pyplot as plt
import numpy as np
import function.interpolation as itp


# Initial conditions and parameters
Pp_initial = 28.4  # Initial pore pressure (in MPa), day 1
temp = 158  # Reservoir temperature in Celsius
max_year_inject = 5  # Maximum injection time in years
max_day_inject = max_year_inject * 365  # Convert years to days
period = np.linspace(1, max_day_inject, 730)  # Time steps over the injection period

bulkvol = 1e12  # Bulk volume of the reservoir
porosity = 0.14  # Reservoir porosity
porevol = porosity * bulkvol  # Pore volume in the reservoir
rhoCO2 = 0.522  # Density of CO2 (in g/cm^3)
injection_rate = 800  # Injection rate in some consistent unit (e.g., m^3/day)

# Initialize variables for simulation
delta_Pp = 0
Pp_post_record = []  # To store post-injection pressure
compressibility_record = []  # Optional: uncomment to store compressibility data

# Reservoir simulation loop
for i in period:
    Pp_post = Pp_initial - delta_Pp  # Calculate the post-injection pressure
    delta_vol = 423782.1 * i  # Example of cumulative injection volume (needs correct units)

    # Interpolate compressibility using the given pressure (Pp_post)
    try:
        compressibility = (itp.interp(Pp_post)[2] * 1e-6) * (1 / 6894.76)  # Convert from psi^-1 to Pa^-1
    except IndexError:
        raise ValueError(f"Invalid interpolation result for pressure {Pp_post} MPa.")

    # Update pressure change based on compressibility and injection volume
    delta_Pp = (1 / porevol) * (delta_vol / compressibility) / 1e6  # Convert to MPa
    Pp_post_record.append(float(Pp_post))  # Record the updated pressure
    # compressibility_record.append(float(compressibility))  # Optionally store compressibility

# Plotting the results
plt.title('Pore Pressure Profile Over Production Time (2014-2019)')
plt.xlabel('Day')
plt.ylabel('Pressure (MPa)')
plt.xlim(1, 365 * 5)  # Set x-axis limit for 5 years
plt.ylim(min(Pp_post_record) * 0.95, Pp_initial * 1.05)  # Set dynamic y-axis limits based on data

plt.plot(period, Pp_post_record, label="Pore Pressure")
plt.legend()
plt.grid(True)
plt.savefig('Pressure_result.png')  # Save the plot as an image
plt.show()  # Display the plot
