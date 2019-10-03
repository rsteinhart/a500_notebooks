"""
Library for thermodynamic functions
"""

def calc_theta(temp,press):
    """
    Parameters
    ----------

      temp: float
        temperature (K)
      press: press float
        pressure (Pa)

    Returns
    -------

      theta: float
         potential temperature (K)
    """
    p0=1.e5
    Rd=287.  #J/kg/K
    cpd=1004.  #J/kg/K
    theta=temp*(p0/press)**(Rd/cpd)
    return theta
