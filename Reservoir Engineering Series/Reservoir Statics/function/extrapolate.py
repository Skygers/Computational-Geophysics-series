import numpy as np
from typing import Tuple

def extrapolate_pressure_gas(sg: float, pressure: float, temp: float, delta: float, z: float) -> Tuple[float, float, float, float]:
    """
    Extrapolates gas pressure above and below a given depth using two different methods.
    by Pandu Hafizh Ananta

    Parameters:
    sg (float): Specific gravity of the gas (must be positive).
    pressure (float): Initial pressure in psia (must be positive).
    temp (float): Temperature in Fahrenheit (must be positive).
    delta (float): Depth increment in feet (can be positive or negative).
    z (float): Compressibility factor (must be between 0 and 1).

    Returns:
    Tuple[float, float, float, float]: Pressure extrapolated below and above using Eq 3.1,
    and pressure extrapolated below and above using Eq 3.7.
    """

    # Validate inputs
    if sg <= 0:
        raise ValueError("Specific gravity (sg) must be positive.")
    if pressure <= 0:
        raise ValueError("Pressure must be positive.")
    if temp <= 0:
        raise ValueError("Temperature must be positive.")
    if not (0 < z <= 1):
        raise ValueError("Compressibility factor (z) must be between 0 and 1.")

    # Constants
    R = 10.732

    # Convert temperature to Rankine once and reuse
    temp_rankine = temp + 459

    # Calculate gas density
    rhogas = (28.97 * sg * pressure) / (z * R * temp_rankine)

    # Gas density gradient
    rhogas_grad = rhogas / 144

    # Extrapolate 
    pressure_extrapolated_below = pressure + rhogas_grad * delta
    pressure_extrapolated_above = pressure - rhogas_grad * delta

    exp_factor = (0.01877 * sg * delta) / (z * temp_rankine)
    pressure_extrapolated_below2 = pressure * np.exp(exp_factor)
    pressure_extrapolated_above2 = pressure * np.exp(-exp_factor)

    return (pressure_extrapolated_below, pressure_extrapolated_above,
            pressure_extrapolated_below2, pressure_extrapolated_above2)
