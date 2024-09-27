import inspect
import sys
sys.path.append("Reservoir Engineering Series\Rock and Fluid Properties")
from utilities import calc_Fahrenheit_to_Rankine, calc_psig_to_psia

class Sutton:
    """
    Class object to calculate pseudo-critical properties based on Sutton's method.

    The model uses Sutton's model (1985) [1]_ to correlate specific gravity (:math:`\gamma_g`) to pseudo-critical pressure (:math:`P_{pc}`) and pseudo-critical
    temperature (:math:`T_{pc}`). It supports corrections for acid gas fractions (:math:`H_2S` and :math:`CO_2`) using
    Wichert & Aziz method (1970) [2]_.
    
    by Pandu Hafizh Ananta
    """

    def __init__(self):
        self.sg = None
        self.T_f = None
        self.T = None
        self.P_g = None
        self.P = None
        self.H2S = None
        self.CO2 = None
        self.Tpc = None
        self.Ppc = None
        self.A = None
        self.B = None
        self.e_correction = None
        self.Tpc_corrected = None
        self.Ppc_corrected = None
        self.Tr = None
        self.Pr = None
        self.ps_props = {
            'Tpc': None,
            'Ppc': None,
            'e_correction': None,
            'Tpc_corrected': None,
            'Ppc_corrected': None,
            'Tr': None,
            'Pr': None,
        }
        self._first_caller_name = None
        self._first_caller_kwargs = {}
        self._first_caller_is_saved = False

    def __str__(self):
        return str(self.ps_props)

    def __repr__(self):
        description = '<gascompressibility.pseudocritical.Sutton> class object with the following calculated attributes:\n{'
        items = '\n   '.join('%s: %s' % (k, v) for k, v in self.ps_props.items())
        return description + '\n   ' + items + '\n}'

    def _calc_A(self, H2S=None, CO2=None):
        self._initialize_H2S(H2S)
        self._initialize_CO2(CO2)
        self.A = self.H2S + self.CO2
        return self.A

    def _calc_B(self, H2S=None):
        self._initialize_H2S(H2S)
        self.B = self.H2S
        return self.B

    def calc_Tpc(self, sg=None):
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_sg(sg)
        self.Tpc = 169.2 + 349.5 * self.sg - 74.0 * self.sg ** 2
        self.ps_props['Tpc'] = self.Tpc
        return self.Tpc

    def calc_Ppc(self, sg=None):
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_sg(sg)
        self.Ppc = 756.8 - 131.07 * self.sg - 3.6 * self.sg ** 2
        self.ps_props['Ppc'] = self.Ppc
        return self.Ppc

    def calc_e_correction(self, H2S=None, CO2=None):
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_A(A=None, H2S=H2S, CO2=CO2)
        self._initialize_B(B=None, H2S=H2S)
        self.e_correction = 120 * (self.A ** 0.9 - self.A ** 1.6) + 15 * (self.B ** 0.5 - self.B ** 4)
        self.ps_props['e_correction'] = self.e_correction
        return self.e_correction

    def calc_Tpc_corrected(self, sg=None, Tpc=None, e_correction=None, H2S=None, CO2=None, ignore_conflict=False):
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_Tpc(Tpc, sg=sg, ignore_conflict=ignore_conflict)

        if e_correction is None and H2S is None and CO2 is None:
            self.Tpc_corrected = self.Tpc
            self.ps_props['Tpc_corrected'] = self.Tpc_corrected
            return self.Tpc_corrected

        self._initialize_e_correction(e_correction, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        self.Tpc_corrected = self.Tpc - self.e_correction
        self.ps_props['Tpc_corrected'] = self.Tpc_corrected
        return self.Tpc_corrected

    def calc_Ppc_corrected(self, sg=None, Tpc=None, Ppc=None, e_correction=None, Tpc_corrected=None, H2S=None, CO2=None, ignore_conflict=False):
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_Ppc(Ppc, sg=sg, ignore_conflict=ignore_conflict)

        if e_correction is None and H2S is None and CO2 is None and Tpc is None and Tpc_corrected is None:
            self.Ppc_corrected = self.Ppc
            self.ps_props['Ppc_corrected'] = self.Ppc_corrected
            return self.Ppc_corrected

        self._initialize_Tpc(Tpc, sg=sg, ignore_conflict=ignore_conflict)
        self._initialize_B(B=None, H2S=H2S)
        self._initialize_e_correction(e_correction, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        self._initialize_Tpc_corrected(Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        self.Ppc_corrected = (self.Ppc * self.Tpc_corrected) / (self.Tpc - self.B * (1 - self.B) * self.e_correction)
        self.ps_props['Ppc_corrected'] = self.Ppc_corrected
        return self.Ppc_corrected

    def calc_Tr(self, T=None, Tpc_corrected=None, sg=None, Tpc=None, e_correction=None, H2S=None, CO2=None, ignore_conflict=False):
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_T(T)
        self._initialize_Tpc_corrected(Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        self.Tr = self.T / self.Tpc_corrected
        self.ps_props['Tr'] = self.Tr
        return self.Tr

    def calc_Pr(self, P=None, Ppc_corrected=None, sg=None, Tpc=None, Ppc=None, e_correction=None, Tpc_corrected=None, H2S=None, CO2=None, ignore_conflict=False):
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_P(P)
        self._initialize_Ppc_corrected(Ppc_corrected, sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction, Tpc_corrected=Tpc_corrected, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        self.Pr = self.P / self.Ppc_corrected
        self.ps_props['Pr'] = self.Pr
        return self.Pr

    def _initialize_sg(self, sg):
        if sg is None:
            if self._first_caller_name in ['calc_Ppc', 'calc_Tpc']:
                raise TypeError("Missing a required argument, sg (specific gravity, dimensionless)")
            else:
                raise TypeError("Missing a required arguments, sg (specific gravity, dimensionless), or Tpc "
                                "(pseudo-critical temperature, °R) or Ppc (pseudo-critical pressure, psia). "
                                "Either both Tpc and Ppc must be inputted, or only sg needs to be inputted.")
        else:
            self.sg = sg

    def _initialize_P(self, P):
        if P is None:
            raise TypeError("Missing a required argument, P (gas pressure, psig)")
        else:
            self.P_a = P  # psia
            self.P = calc_psig_to_psia(P)

    def _initialize_T(self, T):
        if T is None:
            raise TypeError("Missing a required argument, T (gas temperature, °F)")
        else:
            self.T_f = T
            self.T = calc_Fahrenheit_to_Rankine(T)

    def _initialize_H2S(self, H2S):
        self.H2S = 0 if H2S is None else H2S

    def _initialize_CO2(self, CO2):
        self.CO2 = 0 if CO2 is None else CO2

    def _initialize_A(self, A, H2S=None, CO2=None):
        if A is None:
            self._calc_A(H2S=H2S, CO2=CO2)
        else:
            self.A = A

    def _initialize_B(self, B, H2S=None):
        if B is None:
            self._calc_B(H2S=H2S)
        else:
            self.B = B

    def _initialize_Tpc(self, Tpc, sg=None, ignore_conflict=None):
        if Tpc is None:
            self.calc_Tpc(sg=sg)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Tpc, 'Tpc')
            self.Tpc = Tpc

    def _initialize_Ppc(self, Ppc, sg=None, ignore_conflict=None):
        if Ppc is None:
            self.calc_Ppc(sg=sg)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Ppc, 'Ppc')
            self.Ppc = Ppc

    def _initialize_e_correction(self, e_correction, H2S=None, CO2=None, ignore_conflict=False):
        if e_correction is None:
            self.calc_e_correction(H2S=H2S, CO2=CO2)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_e_correction, 'e_correction')
            self.e_correction = e_correction

    def _initialize_Tpc_corrected(self, Tpc_corrected, sg=None, Tpc=None, e_correction=None, H2S=None, CO2=None, ignore_conflict=False):
        if Tpc_corrected is None:
            self.calc_Tpc_corrected(sg=sg, Tpc=Tpc, e_correction=e_correction, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Tpc_corrected, 'Tpc_corrected')
            self.Tpc_corrected = Tpc_corrected

    def _initialize_Ppc_corrected(self, Ppc_corrected, sg=None, Tpc=None, Ppc=None, e_correction=None,
                                  Tpc_corrected=None, H2S=None, CO2=None, ignore_conflict=False):
        if Ppc_corrected is None:
            self.calc_Ppc_corrected(sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction, Tpc_corrected=Tpc_corrected, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Ppc_corrected, 'Ppc_corrected')
            self.Ppc_corrected = Ppc_corrected

    def _initialize_Tr_and_Pr(self, sg=None, P=None, T=None, Tpc=None, Ppc=None, Tpc_corrected=None, Ppc_corrected=None,
               H2S=None, CO2=None, Tr=None, Pr=None, e_correction=None, ignore_conflict=False):
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_Tr(Tr, T, Tpc_corrected=Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, H2S=H2S,
                            CO2=CO2, ignore_conflict=ignore_conflict)
        self._initialize_Pr(Pr, P=P, Ppc_corrected=Ppc_corrected, sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction,
                            Tpc_corrected=Tpc_corrected, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        return self.Tr, self.Pr
    
    def _set_first_caller_attributes(self, func_name, func_kwargs):
        if not self._first_caller_is_saved:
            func_kwargs = {key: value for key, value in func_kwargs.items() if key != 'self'}
            if 'ignore_conflict' in func_kwargs and func_kwargs['ignore_conflict'] is False:
                func_kwargs['ignore_conflict'] = None

            self._first_caller_name = func_name
            self._first_caller_kwargs = func_kwargs
            self._first_caller_is_saved = True

    def _check_conflicting_arguments(self, func, calculated_var):
        args = inspect.getfullargspec(func).args[1:]  
        for arg in args:
            if self._first_caller_kwargs[arg] is not None:
                if self._first_caller_name == '_initialize_Tr_and_Pr':
                    raise TypeError('%s() has conflicting keyword arguments "%s" and "%s"' % ('calc_z', calculated_var, arg))
                raise TypeError('%s() has conflicting keyword arguments "%s" and "%s"' % (self._first_caller_name, calculated_var, arg))
