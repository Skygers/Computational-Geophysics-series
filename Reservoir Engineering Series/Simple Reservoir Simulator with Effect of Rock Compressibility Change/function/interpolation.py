import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import os

pressurenew = np.linspace(1, 100, 100)

def interp(pressurenew, scal_file='data/SCAL.txt'):
    """
    Interpolate SCAL data from a given file.
    
    Parameters:
    pressurenew (array-like): New pressure values to interpolate for.
    scal_file (str): Path to the SCAL data file. Default is './SCAL.txt'.
    
    Returns:
    pressure_scal (array-like): Original pressure values from SCAL data (in MPa).
    K_scal (array-like): Compressibility values from SCAL data.
    compressibility_interp (array-like): Interpolated compressibility values at 'pressurenew'.
    """
    
    # Check if the SCAL file exists
    if not os.path.exists(scal_file):
        raise FileNotFoundError(f"The file {scal_file} was not found.")
    
    # Read SCAL data (assuming the file has two columns: pressure and compressibility)
    scal_data = np.genfromtxt(scal_file)
    
    if scal_data.shape[1] < 2:
        raise ValueError("SCAL data file must contain at least two columns: pressure and compressibility.")
    
    pressure_scal = scal_data[:, 0]  # in psia
    K_scal = scal_data[:, 1]  # Compressibility values
    
    # Convert pressure to MPa
    pressure_scal = pressure_scal * 0.00689  # psia to MPa conversion
    
    # Interpolation using cubic spline
    tck = interpolate.splrep(pressure_scal, K_scal, s=0)
    compressibility_interp = interpolate.splev(pressurenew, tck, der=0)
    
    return pressure_scal, K_scal, compressibility_interp

def plot_interp(pressure_scal, K_scal, pressurenew, compressibility_interp, save_plot=True):
    """
    Plot the SCAL data and the interpolated result.
    
    Parameters:
    pressure_scal (array-like): Original SCAL pressure values (in MPa).
    K_scal (array-like): Original SCAL compressibility values.
    pressurenew (array-like): New pressure values for interpolation.
    compressibility_interp (array-like): Interpolated compressibility values.
    save_plot (bool): If True, save the plot as 'InterpolatedSCAL.png'.
    """
    
    # Plot SCAL data and interpolated results
    plt.plot(pressure_scal, K_scal, 'o', label='Original SCAL Data')
    plt.plot(pressurenew, compressibility_interp, label='Interpolated Data')
    
    plt.title('Compressibility vs. Pressure (Fetkovich, 1998)')
    plt.xlabel('Pressure (MPa)')
    plt.ylabel('Compressibility')
    
    # Adjust plot axis dynamically based on data
    plt.axis([min(pressure_scal), max(pressurenew), min(K_scal), max(K_scal)*1.1])
    
    plt.legend()
    plt.grid(True)
    
    if save_plot:
        plt.savefig('InterpolatedSCAL.png')
        print("Plot saved as 'InterpolatedSCAL.png'")
    else:
        plt.show()

# Uncomment these lines to test the interpolation and plotting
# pressure_scal, K_scal, compressibility_interp = interp(pressurenew)
# plot_interp(pressure_scal, K_scal, pressurenew, compressibility_interp, save_plot=True)
