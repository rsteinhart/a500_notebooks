# %%
import constants as c
import rootfinder as rf
from collections import Iterable
import numpy as np
import pandas as pd


# %%
def find_esat(temp):
    """
    Calculates the saturation water vapor pressure over a flat
    surface of water at temperature 'temp'.

    Parameters
    ----------

    temp : float or array_like
           Temperature of parcel (K).

    Returns
    -------

    esatOut : float or list
        Saturation water vapour pressure (Pa).

    Examples
    --------

    >>> find_esat(300.)
    3534.5196668891358
    >>> find_esat([300., 310.])
    array([ 3534.5197,  6235.5322])

    References
    ----------
    Emanuel 4.4.14 p. 117
      
    """
    # determine if temp has been input as a vector
    is_scalar = True
    if isinstance(temp, Iterable):
        is_scalar = False
    temp = np.atleast_1d(temp)
    Tc = temp - 273.15
    esatOut = 611.2 * np.exp(17.67 * Tc / (Tc + 243.5))
    # if temp is a vector
    if is_scalar:
        esatOut = esatOut[0]
    return esatOut


# %%
def find_rsat(temp, press):
    """
  
   calculate the saturation mixing ratio (kg/kg) at (temp,press)

   Parameters
   --------- 
       
   temp: float
         temperature (K) 

   press: float
         pressure (Pa)

   Returns
   -------
       
    rsat: float
          satruation mixing ratio  (kg/kg)
    """
    esat = find_esat(temp)
    rsat = c.eps * esat / (press - esat)
    return rsat


# %%
def find_resid_rsat(Tguess, rsat, press):
    """

   Calculate residual between target rsat and guess to
   rootfind saturation temperature for constant rsat   
   
   Parameters
   ----------
      
   Tguess: float
           (K) guess temperature from rootfinder 

   rsat:   float
           (kg/kg) target saturation mixing ratio
            
   press:  float
           (hPa) pressure level for rootfind

   Returns
   ------- 
   
   residual: float
             (kg/kg) differnce between target and guess rsat

   Reference
   ---------
      
   see thompkins 2.20
     
    """
    esat = find_esat(Tguess) * 0.01  # convert to hPa
    residual = rsat - c.eps * esat / (press - esat)
    return residual


# %%
def tinvert_rsat(Tstart, rsat, press):
    """
    rootfind the temp that produces rsat at press.

    Parameters
    ----------

    temp : float
           temperature (K)

    rsat : float
           saturation mixing ratio (kg/kg)

    press : float 
            pressure (hPa)

    Returns
    -------

    Tdew : temperature (K) at with air is saaturated
    """
    brackets = rf.find_interval(find_resid_rsat, Tstart, rsat, press)
    temp = rf.fzero(find_resid_rsat, brackets, rsat, press)
    return temp


# %%
def find_lcl(Td, T, p):
    """
    find_lcl(Td, T, p)

    Finds the temperature and pressure at the lifting condensation
    level (LCL) of an air parcel.

    Parameters
    ----------
    Td : float
        Dewpoint temperature (K).

    T : float
        Temperature (K).

    p : float
        Pressure (Pa)

    Returns
    -------

    Tlcl : float
        Temperature at the LCL (K).
    plcl : float
        Pressure at the LCL (Pa).

    Raises
    ------

    NameError
        If the air is saturated at a given Td and T (ie. Td >= T)
    
    Examples
    --------

    >>> [Tlcl, plcl] =  find_lcl(280., 300., 8.e4)
    >>> print(np.array([Tlcl, plcl]))
    [   275.7625  59518.9287]
    >>> find_lcl(300., 280., 8.e4)
    Traceback (most recent call last):
        ...
    NameError: parcel is saturated at this pressure

    References
    ----------
    Emanuel 4.6.24 p. 130 and 4.6.22 p. 129
    
    """
    hit = Td >= T
    if hit is True:
        raise NameError("parcel is saturated at this pressure")

    e = find_esat(Td)
    ehPa = e * 0.01
    # Bolton's formula requires hPa.
    # This is is an empircal fit from for LCL temp from Bolton, 1980 MWR.
    Tlcl = (2840.0 / (3.5 * np.log(T) - np.log(ehPa) - 4.805)) + 55.0

    r = c.eps * e / (p - e)
    cp = c.cpd + r * c.cpv
    logplcl = np.log(p) + cp / (c.Rd * (1 + r / c.eps)) * np.log(Tlcl / T)
    plcl = np.exp(logplcl)

    return Tlcl, plcl


# %%
def calc_lcl(q_bl,theta,psfc):
    """
      find the lcl (in m) for a row in the dataframe
    """
    Tdew = tinvert_rsat(c.Tp, rsat, psfc) #Tstart, rsat, press
    LCL = find_lcl(Tdew,theta,psfc)  #kPa
    #
    # rough approximation:  10 kPa = 1 km
    #
    for item in LCL:
        delp = psfc - item
        lcl_h = delp*100.
    return lcl_h


# %%
esatOut = find_esat(c.Tp)
rsat = find_rsat(c.Tp,c.p0)
#print('esatOut=',esatOut)
#print('rsat=',rsat)

# %%
residual = find_resid_rsat(c.Tp,rsat,c.p0)
Tdew = tinvert_rsat(c.Tp, rsat, c.p0)
#print('Tdew=',Tdew)
#LCL_h = calc_LCL()

# %%
