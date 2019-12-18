# %%
F_theta = Cd*V*(theta_sfc -P[0])
#w_e = A*(Cd*V*(theta_sfc-P[0]) + epsilon*P[0]*Cd*V*(q_sfc - P[1]))/((theta_0 + Gamma*P[2])*(1 + epsilon*q_ft)- P[0])
w_e = A*F_B/delta_theta_v
delta_theta = theta_0 + Gamma*P[2] - P[0]
delta_q = q_ft - P[1]
F_q = Cd*V*(q_sfc - P[1])
delta_theta_v = (theta_0 + Gamma*P[2])*(1 + epsilon*q_ft)- P[0]
F_B = F_theta + epsilon*P[0]*F_q
w_FT = Q_ft/Gamma
w_m = 0 #dry model
#w_m = (-P[2]-LCL)/tau

P[0] = Q_bl + (1/P[2])*(w_e*delta_theta + F_theta)
P[1] = (1/P[2])*(w_e*delta_q + F_q)
P[2] = w_FT + w_e + w_m






