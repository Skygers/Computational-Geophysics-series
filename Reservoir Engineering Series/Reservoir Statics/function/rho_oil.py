from typing import Tuple

def rhooil_grad(so: float, sg: float, Rs: float) -> Tuple[float, float]:
    """
    Calculate the oil density gradient at reservoir conditions.
    by Pandu Hafizh Ananta

    Parameters:
    so (float): Oil specific gravity (must be positive).
    sg (float): Gas specific gravity (must be positive).
    Rs (float): Solution gas-oil ratio in scf/STB (must be positive).

    Returns:
    Tuple[float, float]: Oil density gradient in psi/ft and converted to kPa/m.
    """

    # Constants
    temp_sc = 60.0  # Standard temperature in Fahrenheit
    pressure_sc = 14.73  # Standard pressure in psia
    z_sc = 1.0  # Gas z-factor at standard conditions
    rhowater = 62.366  # Density of water in lbm/ft3
    R = 10.732  # Gas constant in (ft3*psi)/(lb-mol*R)

    # Convert Rs to scf oil/scf gas
    Rs_converted = 940 * (1 / 5.6148)  # Result in scf/STB

    # Oil FVF at surface/standard condition using Standing correlation
    F = Rs * ((sg / so) ** 0.5) + (1.25 * temp_sc)
    Bo = 0.972 + (0.000147 * (F ** 1.1756))

    # Oil density at surface/standard condition
    rhooil_sc = so * rhowater

    # Gas density at surface/standard condition using real-gas law
    temp_rankine_sc = temp_sc + 459.67
    rhogas_sc = (28.97 * sg * pressure_sc) / (z_sc * R * temp_rankine_sc)

    # Oil density at reservoir condition
    rhooil = (rhooil_sc + (rhogas_sc * Rs_converted)) / Bo

    # Oil density gradient calculations
    rhooil_grad = rhooil / 144.0  # Convert from lbm/ft3 to psi/ft
    rhooil_grad_converted = rhooil_grad * (6.89476 / 0.3048)  # Convert from psi/ft to kPa/m

    return rhooil_grad, rhooil_grad_converted
