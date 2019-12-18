from scipy.integrate import odeint
import constants as c
from solv_eqns_final import solve_equations
import numpy as np

Q_bl = [-1,-2,-3,-4,-5,-6]
prof = np.empty_like(Q_bl)
for elem in Q_bl:
    prof_elem = odeint(solve_equations, c.P0, c.tspan, elem)
    prof = prof.append(prof_elem)
return prof




