"""
Fluid Replacement Modelling, Gassmann (1951)
by Pandu Hafizh Ananta
"""

def Ks(Kd, Km, Kf, phi):
    """
    Calculate the saturated bulk modulus (Ks) using Gassmann's equation.
    
    Parameters:
    Kd (float): Dry rock bulk modulus
    Km (float): Mineral bulk modulus
    Kf (float): Fluid bulk modulus
    phi (float): Porosity
    
    Returns:
    float: Saturated bulk modulus (Ks)
    """
    # Ensure Km and Kf are non-zero to avoid division by zero errors
    if Km == 0 or Kf == 0:
        raise ValueError("Mineral bulk modulus (Km) and fluid bulk modulus (Kf) must be non-zero.")
    
    gamma = 1.0 - phi - Kd / Km
    Ks = Kd + ((gamma + phi) ** 2) / (gamma / Km + phi / Kf)
    
    return Ks


def Kd(Ks, Km, Kf, phi):
    """
    Calculate the dry bulk modulus (Kd) from the saturated bulk modulus (Ks).
    
    Parameters:
    Ks (float): Saturated bulk modulus
    Km (float): Mineral bulk modulus
    Kf (float): Fluid bulk modulus
    phi (float): Porosity
    
    Returns:
    float: Dry bulk modulus (Kd)
    """
    # Ensure Km and Kf are non-zero to avoid division by zero errors
    if Km == 0 or Kf == 0:
        raise ValueError("Mineral bulk modulus (Km) and fluid bulk modulus (Kf) must be non-zero.")
    
    gamma = phi * (Km / Kf - 1.0)
    Kd = (Ks * (gamma + 1.0) - Km) / (gamma - 1.0 + Ks / Km)
    
    return Kd
