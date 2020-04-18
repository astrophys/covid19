# Author : Ali Snedden
# Date   : 4/12/20
# License: MIT
# Purpose: 
#   This code attmpts to follow OSU / IDI∗ COVID-19 Response Modeling Team's white paper.
#   
#
#   
# Notes : 
#   
# References : 
#   1. https://idi.osu.edu/assets/pdfs/covid_response_white_paper.pdf
#   2. https://mbi.osu.edu/events/seminar-grzegorz-rempala-mathematical-models-epidemics-tracking-coronavirus-using-dynamic
#
# Future:
#   
#
#
import sys
import numpy as np
import time
import pandas as pd
from matplotlib import pyplot as plt
from error import exit_with_error
import random
random.seed(42)     # Change later
from classes import AGENT

def print_help(ExitCode):
    """
    ARGS:
    RETURN:
    DESCRIPTION:
    DEBUG:
    FUTURE:
    """
    sys.stderr.write(
        "python3 ./src/osu_ide_replication_attempt.py R0 inc_time infect_time \n"
        "      R0          : How many people on average person infects\n"
        "      inc_time    : Incubation time (days)\n"
        "      infect_time : Time after infection person becomes infectious \n"
        "      \n"
        "      \n"
        "   To Run: \n"
        "   source ~/.local/virtualenvs/python3.7/bin/activate\n")
    sys.exit(ExitCode)



#
# Below are a series of functions. I'm excluding the normal information (e.g. ARGS,
# RETURN, DESCRIPTION, DEBUG, FUTURE) that I typically include in function prototypes b/c
# they are all basically the same.
#       ARGS   : 
#           Beta  = Rate of infecting nearby neighbors
#           Delta = Voluntary Quarantine rate
#           Kappa = Avg contact network density, if = 1 implies Poisson degree assumption
#           Gamma = Rate of recovery
#           Mu    = Average number of node's contacts.
#           X_D   = Relative density of infectious connections. = x_SI / x_S
#           X_S   = Relative number of susceptibles
#           X_I   = Relative number of infected.
#
#       RETURN : 
#       DESCRIPTION :
#           Below functions are derived from Appendix A
#       DEBUG  : 
#       FUTURE :
#
def f_D(Beta=None,Delta=None,Kappa=None, Gamma=None, Mu=None, X_D=None, X_S=None, X_I=None):
    """
    DESCRIPTION:
        Rate of change w/r/t time of relative number infected. From equation 4.1, 
    """
    gammaT = Beta + Gamma + Delta   # Gamma Tilde
    return(Beta*(1-Kappa)*X_D**2 + (Kappa * Mu * Beta * X_S**(2*Kappa - 1) - gammaT)*X_D)


def f_S(Beta=None,Delta=None,Kappa=None, Gamma=None, Mu=None, X_D=None, X_S=None, X_I=None):
    """
    DESCRIPTION:
        Rate of change w/r/t time of relative number susceptibles. From equation 4.1, 
    """
    return(-Beta * X_D * X_S)


def f_I(Beta=None,Delta=None,Kappa=None, Gamma=None, Mu=None, X_D=None, X_S=None, X_I=None):
    """
    DESCRIPTION:
        Rate of change w/r/t time of relative number infected. From equation 4.1, 
    """
    return(Beta * X_D * X_S - Gamma * X_I)


def k1(Funct=None, H=None, Beta=None, Delta=None, Kappa=None, Gamma=None, Mu=None,
       X_D=None, X_S=None, X_I=None
):
    """
    ARGS:
        Funct : Function, either f_D(), f_S(), f_I()
    RETURN:
        k1_i for the 4th order Runge-Kutta. _i determined by function passed.
    DESCRIPTION:
    DEBUG:
    FUTURE:
    """
    return(H * Funct(Beta, Delta, Kappa, Gamma, Mu, X_D, X_S, X_I))


def k2(K1D=None, Funct=None, H=None, Beta=None, Delta=None, Kappa=None, Gamma=None, Mu=None,
       X_D=None, X_S=None, X_I=None
):
    """
    ARGS:
        K1D   : Dictionary of K1 values, keys : X_D, X_S, X_I
        Funct : Function, either f_D(), f_S(), f_I()
    RETURN:
    DESCRIPTION:
    """
    # No explicit time dependence in functions, so don't worry about it.
    k1_D = K1D["X_D"]
    k1_S = K1D["X_S"]
    k1_I = K1D["X_I"]
    xD = X_D + 0.5 * k1_D
    xS = X_S + 0.5 * k1_S
    xI = X_I + 0.5 * k1_I
    return(H * Funct(Beta, Delta, Kappa, Gamma, Mu, xD, xS, xI))


def k3(K2D=None, Funct=None, H=None, Beta=None, Delta=None, Kappa=None, Gamma=None, Mu=None,
       X_D=None, X_S=None, X_I=None
):
    """
    ARGS:
        K2D   : Dictionary of K2 values, keys : X_D, X_S, X_I
        Funct : Function, either f_D(), f_S(), f_I()
    RETURN:
    DESCRIPTION:
    """
    k2_D = K2D["X_D"]
    k2_S = K2D["X_S"]
    k2_I = K2D["X_I"]
    xD = X_D + 0.5 * k2_D
    xS = X_S + 0.5 * k2_S
    xI = X_I + 0.5 * k2_I
    return(H * Funct(Beta, Delta, Kappa, Gamma, Mu, xD, xS, xI))


def k4(K3D=None, Funct=None, H=None, Beta=None, Delta=None, Kappa=None, Gamma=None, Mu=None,
       X_D=None, X_S=None, X_I=None
):
    """
    ARGS:
        K3D   : List of K2 values, ordered by X_D, X_S, X_I
        Funct : Function, either f_D(), f_S(), f_I()
    RETURN:
    DESCRIPTION:
    """
    k3_D = K3D["X_D"]
    k3_S = K3D["X_S"]
    k3_I = K3D["X_I"]
    xD = X_D + k3_D
    xS = X_S + k3_S
    xI = X_I + k3_I
    return(H * Funct(Beta, Delta, Kappa, Gamma, Mu, xD, xS, xI))


def main():
    """
    ARGS:
    RETURN:
    DESCRIPTION:
    DEBUG:
    FUTURE:
        1. Add option to fit only a specific section of data.
    """
    # Check Python version
    nArg = len(sys.argv)
    # Use python 3
    if(sys.version_info[0] != 3):
        exit_with_error("ERROR!!! Use Python 3\n")
    # Get options 
    if("-h" in sys.argv[1]):
        print_help(0)
    elif(nArg != 4):
        print_help(1)

    startTime = time.time()
    print("{} \n".format(sys.argv),flush=True)
    print("   Start Time : {}".format(time.strftime("%a, %d %b %Y %H:%M:%S ",
                                       time.localtime())),flush=True)
    
    ## Get args
    kappa = 1      # =1 is Poisson, >1 is negative binomial. Average contact network density
    beta  = 0.1    # constant rate of infection
    gamma = 0.1    # average recovery rate
    mu = 3         # average number of nodes contacts
    delta = 0.1    # quarantine 
    rho=1
    R0 = kappa * beta / gamma
    #R0         = float(sys.argv[1])    # Average number of people infected
    #incubTime  = float(sys.argv[2])    # Time before symptoms present
    #infectTime = float(sys.argv[3])    # Time before infectious
    #deathRate  = 0.01           # fraction of infected that die
    #hostRate   = 0.20           # Fraction that get hospitalized
    #healthyTime= 8             # Time after infection that person is healthy and no longer infectious
    #nDays      = 100
    ##sd         = 5              # Standard deviation for gaussian distribution for infection
    N = 10**3       # Number of agents

    # Initial Conditions
    xS = 1
    xI = rho
    xD = mu * rho


    print("Ended : %s"%(time.strftime("%D:%H:%M:%S")))
    print("Run Time : {:.4f} h".format((time.time() - startTime)/3600.0))



    sys.exit(0)


if __name__ == "__main__":
    main()
