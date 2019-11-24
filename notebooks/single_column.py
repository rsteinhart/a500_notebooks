#
# Input paramters
#
Q_bl = [-1.0, -2.0, -3.0, -4.0, -5.0, -6.0] #K day^-1
Q_ft = -1.0 #K day^-1
Gamma = 5.0 #K km^-1
theta_0 = 298 #K
theta_sfc = 301 #K
A = 0.41
Cd = 0.001
V = 5 #m/s
tau = 15 #min
epsilon = 0.61

h = 400 #height of BL [m]
theta_sfc = 302 #K
w_e = A*F_b/delta_theta_v #entrainment velocity
w_ft = Q_ft/Gamma
if LCL<h:
    w_m = -(h-LCL)/tau
else:
    w_m = 0

F_0 = Cd*V*(theta_sfc - theta_bl)
delta_theta = theta_0 + Gamma*h - theta_bl
d_theta_bl_dt = Q_bl + (1/h)*(w_e*delta_theta + F_theta)

dq_bl_dt = (1/h)*(w_e*delta_q + F_q)
#delta_q = q_FT - q_BL
delta_q = 3 #g/kg for q_bl >=3 g/kg
F_q = Cd*V(q_sfc - q_bl)

dh_dt =  w_ft + w_e + w_m
delta_theta_v = (theta_0 + Gamma*h)*(1+ epsilon*q_ft) - theta_v_bl
F_b = F_theta + epsilon*theta_bl*F_q
