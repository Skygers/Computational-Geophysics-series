# function/compressibilities/dranchuk_kaseem.py
import numpy as np

"""
Dranchuk, P.M., and Abou-Kassem, J.H.: "Calculation of z-Factors for Natural Gases Using Equations of State," 
Journal of Canadian Petroleum Technology (1975)

https://onepetro.org/JCPT/article-abstract/doi/10.2118/75-03-03
"""


def DAK(z: float, Pr: float, Tr: float) -> float:
    """
    Calculates the compressibility factor (z-factor) for natural gases
    using the Dranchuk-Abou-Kassem equation of state.

    Parameters:
    z (float): Initial estimate of z-factor.
    Pr (float): Reduced pressure.
    Tr (float): Reduced temperature.

    Returns:
    float: The calculated z-factor.
    """
    # Constants
    A1, A2, A3, A4, A5 = 0.3265, -1.0700, -0.5339, 0.01569, -0.05165
    A6, A7, A8, A9, A10, A11 = 0.5475, -0.7361, 0.1844, 0.1056, 0.6134, 0.7210

    #expression components
    Pr_Tr = (0.27 * Pr) / (z * Tr)
    Tr_inv = 1 / Tr
    Pr_Tr_sq = Pr_Tr ** 2
    Pr_Tr_5 = Pr_Tr ** 5
    exp_term = np.exp(-A11 * Pr_Tr_sq)

    # Calculating
    term1 = (A1 + A2 * Tr_inv + A3 * Tr_inv**3 + A4 * Tr_inv**4 + A5 * Tr_inv**5) * Pr_Tr
    term2 = (A6 + A7 * Tr_inv + A8 * Tr_inv**2) * Pr_Tr_sq
    term3 = -A9 * (A7 * Tr_inv + A8 * Tr_inv**2) * Pr_Tr_5
    term4 = A10 * (1 + A11 * Pr_Tr_sq) * (Pr_Tr_sq / Tr**3) * exp_term

    #result
    result = 1 + term1 + term2 + term3 + term4 - z

    return result


# Example usage (for testing purposes)
# if __name__ == "__main__":
#     z_initial = 0.9
#     Pr = 1.5
#     Tr = 2.0
#     z_factor = calculate_z_factor(z_initial, Pr, Tr)
#     print(f"Calculated z-factor: {z_factor}")
