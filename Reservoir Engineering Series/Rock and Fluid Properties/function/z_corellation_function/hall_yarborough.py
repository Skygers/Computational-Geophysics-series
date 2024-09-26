import numpy as np

"""
Hall, K.R., and Yarborough, L.: "A new equation of state for Z-factor calculations," Oil and Gas Journal (1973)
https://www.researchgate.net/publication/284299884_A_new_equation_of_state_for_Z-factor_calculations
"""


def hall_yarborough(z: float, Pr: float, Tr: float) -> float:
    """
    Calculates the Z-factor using the Hall-Yarborough equation of state.

    Parameters:
    z (float): Initial estimate of Z-factor.
    Pr (float): Reduced pressure.
    Tr (float): Reduced temperature.

    Returns:
    float: The calculated Z-factor.
    """

    t = 1 / Tr

    # Coefficients based on reduced temperature
    A1 = 0.06125 * t * np.exp(-1.2 * (1 - t) ** 2)
    A2 = 14.76 * t - 9.76 * t ** 2 + 4.58 * t ** 3
    A3 = 90.7 * t - 242.2 * t ** 2 + 42.4 * t ** 3
    A4 = 2.18 + 2.82 * t
    #component
    A1_Pr_z = (A1 * Pr) / z
    # calculation terms
    term1 = -A1 * Pr
    term2 = (A1_Pr_z + A1_Pr_z ** 2 + A1_Pr_z ** 3 - A1_Pr_z ** 4) / (1 - A1_Pr_z) ** 3
    term3 = -A2 * A1_Pr_z ** 2
    term4 = A3 * A1_Pr_z ** A4
    # Return
    result = term1 + term2 + term3 + term4

    return result

# Example usage (for testing purposes)
# if __name__ == "__main__":
#     z_initial = 0.9
#     Pr = 1.5
#     Tr = 2.0
#     z_factor = hall_yarborough(z_initial, Pr, Tr)
#     print(f"Calculated Z-factor: {z_factor}")
