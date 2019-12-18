def solve_equations(P,t, Q_ft, Gamma, theta_0, theta_sfc, A, Cd, V, tau, epsilon, Q_bl, q_sfc, q_ft, q_bl, LCL):
    #
    # "EQUATIONS"
    #
    P[0] = Q_bl + (1/P[2])*((A*(Cd*V*(theta_sfc-P[0]) + epsilon*P[0])*Cd*V*(q_sfc - P[1]))/((theta_0 + Gamma*P[2])*(1 + epsilon*q_ft)- P[0]) + Cd*V*(theta_sfc -P[0]))
    P[1] = (1/P[2])*(A*((Cd*V*(theta_sfc-P[0]) + epsilon*P[0])*Cd*V*(q_sfc - P[1]))*(q_ft - P[1]) + Cd*V*(q_sfc - P[1]))
    P[2] = (Q_ft/Gamma) + (A*((Cd*V*(theta_sfc - P[0]) + epsilon*P[0]*Cd*V*(q_sfc - q_bl))/((theta_0 + Gamma*P[2])*(1+epsilon*q_ft)-P[0]))) + (-P[2]-LCL)/tau
   
    return(P[0], P[1], P[2])
