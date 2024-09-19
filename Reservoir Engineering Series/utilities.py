'''
Conversion units

Contains functions for converting units.
Each function will take in a value in one unit and return the equivalent value in another unit.
by Pandu Hafizh Ananta
'''

def api_to_density(api: float) -> float:
    """Convert API gravity to density in g/cm³"""
    return 141.4 / (131.5 + api)

def atm_to_pa(atm: float) -> float:
    """Convert atmosphere (atm) to Pascals (Pa)"""
    return atm * 1.013250E+05

def bbl_to_m3(bbl: float) -> float:
    """Convert barrels (bbl) to cubic meters (m³)"""
    return bbl * 1.589873E-01

def cp_to_pa_s(cp: float) -> float:
    """Convert centipoise (cp) to Pascal-seconds (Pa·s)"""
    return cp * 1E-03

def darcy_to_micro_m2(darcy: float) -> float:
    """Convert darcy to micro square meters (μm²)"""
    return darcy * 9.869233

def dyne_to_mn(dyne: float) -> float:
    """Convert dyne to millinewtons (mN)"""
    return dyne * 1E-02

def dyne_cm_to_psi_cm(dyne_cm: float) -> float:
    """Convert dyne/cm to psi/cm"""
    return dyne_cm / 68947.57

def dyne_cm2_to_pa(dyne_cm2: float) -> float:
    """Convert dyne/cm² to Pascals (Pa)"""
    return dyne_cm2 * 1E-01

def ft_to_m(ft: float) -> float:
    """Convert feet (ft) to meters (m)"""
    return ft * 3.048E-01

def ft2_to_m2(ft2: float) -> float:
    """Convert square feet (ft²) to square meters (m²)"""
    return ft2 * 9.290304E-02

def ft3_to_m3(ft3: float) -> float:
    """Convert cubic feet (ft³) to cubic meters (m³)"""
    return ft3 * 2.831685E-02

def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit (°F) to Celsius (°C)"""
    return (f - 32) / 1.8

def fahrenheit_to_kelvin(f: float) -> float:
    """Convert Fahrenheit (°F) to Kelvin (K)"""
    return (f + 459.67) / 1.8

def milidarcy_to_micro_m2(md: float) -> float:
    """Convert millidarcy to micro square meters (μm²)"""
    return md * 9.869233E-04

def in_to_cm(inches: float) -> float:
    """Convert inches (in) to centimeters (cm)"""
    return inches * 2.54

def in2_to_cm2(in2: float) -> float:
    """Convert square inches (in²) to square centimeters (cm²)"""
    return in2 * 6.4516

def in3_to_cm3(in3: float) -> float:
    """Convert cubic inches (in³) to cubic centimeters (cm³)"""
    return in3 * 1.638706

def lbf_to_n(lbf: float) -> float:
    """Convert pound-force (lbf) to Newtons (N)"""
    return lbf * 4.448706

def lbm_to_kg(lbm: float) -> float:
    """Convert pound-mass (lbm) to kilograms (kg)"""
    return lbm * 4.535924E-01

def psi_to_kpa(psi: float) -> float:
    """Convert psi to kilopascals (kPa)"""
    return psi * 6.894757

def psi_inv_to_kpa_inv(psi_inv: float) -> float:
    """Convert psi⁻¹ to kPa⁻¹"""
    return psi_inv * 1.450377E-01

def rankine_to_kelvin(r: float) -> float:
    """Convert Rankine (°R) to Kelvin (K)"""
    return r * 5/9

def acre_to_ha(acre: float) -> float:
    """Convert acres to hectares (ha)"""
    return acre * 4.046E-01

def acre_ft_to_m(acre_ft: float) -> float:
    """Convert acre-feet to meters (m³)"""
    return acre_ft * 1.233489E+03

def mile_to_km(mile: float) -> float:
    """Convert miles to kilometers (km)"""
    return mile * 1.609344

def sq_mile_to_km2(sq_mile: float) -> float:
    """Convert square miles to square kilometers (km²)"""
    return sq_mile * 2.589988

def scf_to_ft3(scf: float) -> float:
    """Convert standard cubic feet (scf) to cubic feet (ft³)"""
    return scf

def stb_to_bbl(stb: float) -> float:
    """Convert stock tank barrel (stb) to barrels (bbl)"""
    return stb

def tscf_to_scf(tscf: float) -> float:
    """Convert trillion standard cubic feet (Tscf) to standard cubic feet (scf)"""
    return tscf * 1E+12

def mmstb_to_stb(mmstb: float) -> float:
    """Convert million stock tank barrels (MMstb) to stock tank barrels (stb)"""
    return mmstb * 1E+06
