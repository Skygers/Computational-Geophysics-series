import numpy as np

"""
Kareem, L.A., Iwalewa, T.M., and Marhoun, M.al-.,: "New explicit correlation for the compressibility factor of natural gas: linearized z-factor isotherms," 
Journal of Petroleum Exploration and Production Technology (2016)

https://link.springer.com/article/10.1007/s13202-015-0209-3
"""


def kareem(Pr: float, Tr: float) -> float:
    """
    Calculates the z-factor using the Kareem et al. (2016) equation of state.

    Parameters:
    Pr (float): Reduced pressure.
    Tr (float): Reduced temperature.

    Returns:
    float: The calculated z-factor.
    """

    # Coefficients for the Kareem equation
    a1, a2, a3, a4, a5 = 0.317842, 0.382216, -7.768354, 14.290531, 0.000002
    a6, a7, a8, a9, a10 = -0.004693, 0.096254, 0.166720, 0.966910, 0.063069
    a11, a12, a13, a14, a15 = -1.966847, 21.0581, -27.0246, 16.23, 207.783
    a16, a17, a18, a19 = -488.161, 176.29, 1.88453, 3.05921

    # Temperature-dependent term
    t = 1 / Tr

    # Equation terms
    A = a1 * t * np.exp(a2 * (1 - t) ** 2) * Pr
    B = a3 * t + a4 * t ** 2 + a5 * t ** 6 * Pr ** 6
    C = a9 + a8 * t * Pr + a7 * t ** 2 * Pr ** 2 + a6 * t ** 3 * Pr ** 3
    D = a10 * t * np.exp(a11 * (1 - t) ** 2)

    # Components E, F, G
    E = a12 * t + a13 * t ** 2 + a14 * t ** 3
    F = a15 * t + a16 * t ** 2 + a17 * t ** 3
    G = a18 + a19 * t

    # Intermediate variable y
    y = (D * Pr) / (((1 + A ** 2) / C) - ((A ** 2 * B) / C ** 3))

    # Final result for z-factor
    z_factor = (D * Pr * (1 + y + y ** 2 - y ** 3)) / (
        (D * Pr + E * y ** 2 - F * y ** G) * (1 - y) ** 3
    )

    return z_factor

# Example usage (for testing purposes)
# if __name__ == "__main__":
#     Pr = 3.0153
#     Tr = 1.6155
#     z_factor = kareem(Pr, Tr)
#     print(f"Calculated Z-factor: {z_factor}")
