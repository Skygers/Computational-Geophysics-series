import numpy as np
import inspect
import sys

sys.path.append("Reservoir Engineering Series")
from utilities import calc_Fahrenheit_to_Rankine, calc_psig_to_psia

class Piper:
    """
    Class object to calculate pseudo-critical properties based on Piper's method (1993).
    Supports corrections for acid gas fractions (H2S, CO2, N2).
    by Pandu Hafizh Ananta
    """

    def __init__(self):
        # Initialize all necessary properties
        self.sg = self.T_f = self.T = self.P_g = self.P = None
        self.H2S = self.CO2 = self.N2 = 0.0  # Default mole fractions
        self.Tpc = self.Ppc = self.J = self.K = self.Tr = self.Pr = None

        # Constants for pseudo-critical properties of gases
        self.Pc_H2S, self.Tc_H2S = 1306, 672.3
        self.Pc_CO2, self.Tc_CO2 = 1071, 547.5
        self.Pc_N2, self.Tc_N2 = 492.4, 227.16

        # Dictionary for calculated pseudo-critical properties
        self.ps_props = {
            'Tpc': None, 'Ppc': None, 'J': None, 'K': None, 'Tr': None, 'Pr': None
        }

        # Caller tracking for conflict resolution
        self._first_caller_name = None
        self._first_caller_kwargs = {}
        self._first_caller_is_saved = False

    def __repr__(self):
        return f"<Piper Object: Pseudo-critical properties {self.ps_props}>"

    def calc_J(self, sg=None, H2S=None, CO2=None, N2=None):
        """ Calculates Stewart-Burkhardt-VOO parameter J (°R/psia). """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_components(sg, H2S, CO2, N2)
        self.J = (0.11582 - 0.45820 * self.H2S * (self.Tc_H2S / self.Pc_H2S) 
                 - 0.90348 * self.CO2 * (self.Tc_CO2 / self.Pc_CO2)
                 - 0.66026 * self.N2 * (self.Tc_N2 / self.Pc_N2) 
                 + 0.70729 * self.sg - 0.099397 * self.sg ** 2)
        self.ps_props['J'] = self.J
        return self.J

    def calc_K(self, sg=None, H2S=None, CO2=None, N2=None):
        """ Calculates Stewart-Burkhardt-VOO parameter K (°R/psia^0.5). """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_components(sg, H2S, CO2, N2)
        self.K = (3.8216 - 0.06534 * self.H2S * (self.Tc_H2S / np.sqrt(self.Pc_H2S)) 
                 - 0.42113 * self.CO2 * (self.Tc_CO2 / np.sqrt(self.Pc_CO2)) 
                 - 0.91249 * self.N2 * (self.Tc_N2 / np.sqrt(self.Pc_N2)) 
                 + 17.438 * self.sg - 3.2191 * self.sg ** 2)
        self.ps_props['K'] = self.K
        return self.K

    def calc_Tpc(self, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None, ignore_conflict=False):
        """ Calculates pseudo-critical temperature Tpc (°R). """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_J_and_K(J, K, sg, H2S, CO2, N2, ignore_conflict)
        self.Tpc = self.K ** 2 / self.J
        self.ps_props['Tpc'] = self.Tpc
        return self.Tpc

    def calc_Ppc(self, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None, Tpc=None, ignore_conflict=False):
        """ Calculates pseudo-critical pressure Ppc (psia). """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        if Tpc is not None:
            if K is not None:
                raise TypeError(f'{self._first_caller_name} has conflicting arguments: "Tpc" and "K"')
            self.Tpc = Tpc
        else:
            self._initialize_Tpc(sg, H2S, CO2, N2, J, K, ignore_conflict)
        self.Ppc = self.Tpc / self.J
        self.ps_props['Ppc'] = self.Ppc
        return self.Ppc

    def calc_Tr(self, T=None, sg=None, Tpc=None, H2S=None, CO2=None, N2=None, J=None, K=None, ignore_conflict=False):
        """ Calculates pseudo-reduced temperature Tr (dimensionless). """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_T(T)
        self._initialize_Tpc(sg, H2S, CO2, N2, J, K, ignore_conflict)
        self.Tr = self.T / self.Tpc
        self.ps_props['Tr'] = self.Tr
        return self.Tr

    def calc_Pr(self, P=None, sg=None, Tpc=None, Ppc=None, H2S=None, CO2=None, N2=None, J=None, K=None, ignore_conflict=False):
        """ Calculates pseudo-reduced pressure Pr (dimensionless). """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_P(P)
        self._initialize_Ppc(sg, H2S, CO2, N2, J, K, Tpc, ignore_conflict)
        self.Pr = self.P / self.Ppc
        self.ps_props['Pr'] = self.Pr
        return self.Pr

    def _initialize_components(self, sg, H2S, CO2, N2):
        """ Helper to initialize sg, H2S, CO2, N2. """
        self.sg = sg if sg is not None else self.sg
        self.H2S = H2S if H2S is not None else 0.0
        self.CO2 = CO2 if CO2 is not None else 0.0
        self.N2 = N2 if N2 is not None else 0.0

    def _initialize_T(self, T):
        if T is None:
            raise TypeError("Missing argument: T (temperature, °F)")
        self.T_f = T
        self.T = calc_Fahrenheit_to_Rankine(T)

    def _initialize_P(self, P):
        if P is None:
            raise TypeError("Missing argument: P (pressure, psig)")
        self.P_g = P
        self.P = calc_psig_to_psia(P)

    def _initialize_J_and_K(self, J, K, sg, H2S, CO2, N2, ignore_conflict):
        """ Helper to initialize J and K values. """
        if J is None:
            self.calc_J(sg, H2S, CO2, N2)
        else:
            if not ignore_conflict:
                self._check_conflicting_arguments(self.calc_J, 'J')
            self.J = J
        if K is None:
            self.calc_K(sg, H2S, CO2, N2)
        else:
            if not ignore_conflict:
                self._check_conflicting_arguments(self.calc_K, 'K')
            self.K = K

    def _check_conflicting_arguments(self, func, var_name):
        """ Raises conflict error if a parameter was set more than once. """
        if self._first_caller_kwargs.get(var_name) is not None:
            raise TypeError(f'{self._first_caller_name} has conflicting arguments: "{var_name}"')

    def _set_first_caller_attributes(self, func_name, func_kwargs):
        """ Tracks the first caller and its arguments to handle conflicts. """
        if not self._first_caller_is_saved:
            self._first_caller_name = func_name
            self._first_caller_kwargs = {k: v for k, v in func_kwargs.items() if k != 'self'}
            self._first_caller_is_saved = True
    
    def _initialize_Tr_and_Pr(self, sg=None, P=None, T=None, Tpc=None, Ppc=None, Tpc_corrected=None, Ppc_corrected=None,
                          H2S=None, CO2=None, Tr=None, Pr=None, e_correction=None, ignore_conflict=False):
        """
        Initializes both pseudo-reduced temperature (Tr) and pseudo-reduced pressure (Pr) 
        based on the provided or computed values.
    
        Parameters
        ----------
        sg : float
        Specific gravity of the gas.
        P : float
            Gas pressure (psig).
        T : float
            Gas temperature (°F).
        Tpc : float
            Pseudo-critical temperature (°R).
        Ppc : float
            Pseudo-critical pressure (psia).
        Tpc_corrected : float
            Corrected pseudo-critical temperature (°R).
        Ppc_corrected : float
            Corrected pseudo-critical pressure (psia).
        H2S : float
            Mole fraction of H2S (dimensionless).
        CO2 : float
            Mole fraction of CO2 (dimensionless).
        Tr : float
            Pseudo-reduced temperature (dimensionless).
        Pr : float
            Pseudo-reduced pressure (dimensionless).
        e_correction : float
            Temperature-correction factor for acid gases (°R).
        ignore_conflict : bool
            If set to True, will ignore conflicting values.

        Returns
        -------
        Tuple[float, float]
            Returns the pseudo-reduced temperature (Tr) and pseudo-reduced pressure (Pr).
            """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_Tr(Tr, T, Tpc_corrected=Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, H2S=H2S,
                        CO2=CO2, ignore_conflict=ignore_conflict)
        self._initialize_Pr(Pr, P=P, Ppc_corrected=Ppc_corrected, sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction,
                        Tpc_corrected=Tpc_corrected, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        return self.Tr, self.Pr
