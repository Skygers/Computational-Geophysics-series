import numpy as np

"""
Londono, F.E., Archer, R.A., and Blasingame, T.A.: 
"Simplified Correlations for Hydrocarbon Gas Viscosity and Gas Density — Validation and Correlation of Behavior 
Using a Large-Scale Database," paper SPE 75721 (2005)

https://onepetro.org/SPEGTS/proceedings/02GTS/All-02GTS/SPE-75721-MS/135705
"""


def londono(z: float, Pr: float, Tr: float) -> float:
    """
    Calculates the z-factor using the Londono et al. (2005) equation of state.

    Parameters:
    z (float): Initial estimate of z-factor.
    Pr (float): Reduced pressure.
    Tr (float): Reduced temperature.

    Returns:
    float: The calculated z-factor.
    """
    
    # Constants from the Londono et al. equation
    A1, A2, A3, A4, A5 = 0.3024696, -1.046964, -0.1078916, -0.7694186, 0.1965439
    A6, A7, A8, A9, A10, A11 = 0.6527819, -1.118884, 0.3951957, 0.09313593, 0.8483081, 0.7880011

    # Reusable components
    Pr_Tr = (0.27 * Pr) / (z * Tr)
    Pr_Tr_sq = Pr_Tr ** 2
    Pr_Tr_5 = Pr_Tr ** 5
    exp_term = np.exp(-A11 * Pr_Tr_sq)

    # Calculating terms
    term1 = (A1 + A2 / Tr + A3 / Tr ** 3 + A4 / Tr ** 4 + A5 / Tr ** 5) * Pr_Tr
    term2 = (A6 + A7 / Tr + A8 / Tr ** 2) * Pr_Tr_sq
    term3 = -A9 * (A7 / Tr + A8 / Tr ** 2) * Pr_Tr_5
    term4 = A10 * (1 + A11 * Pr_Tr_sq) * (Pr_Tr_sq / Tr ** 3) * exp_term

    # Final z-factor calculation
    result = 1 + term1 + term2 + term3 + term4 - z

    return result


# Example usage (for testing purposes)
# if __name__ == "__main__":
#     z_initial = 0.9
#     Pr = 1.5
#     Tr = 2.0
#     z_factor = londono(z_initial, Pr, Tr)
#     print(f"Calculated Z-factor: {z_factor}")
