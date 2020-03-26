# Author : Ali Snedden
# Date   : 3/21/20
# License: MIT
# Purpose: 
#   This code naively simulates an Agent based model.
#   
#
#   
# Notes : 
#   
# References : 
#   1. https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-NPI-modelling-16-03-2020.pdf
# 
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
        "python3 ./src/simulatoin.py R0 inc_time infect_time \n"
        "      R0          : How many people on average person infects\n"
        "      inc_time    : Incubation time (days)\n"
        "      infect_time : Time after infection person becomes infectious \n"
        "      \n"
        "      \n"
        "   To Run: \n"
        "   source ~/.local/virtualenvs/python3.7/bin/activate\n")
    sys.exit(ExitCode)


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
    
    # Get args
    R0         = float(sys.argv[1])    # Average number of people infected
    incubTime  = float(sys.argv[2])    # Time before symptoms present
    infectTime = float(sys.argv[3])    # Time before infectious
    deathRate  = 0.01           # fraction of infected that die
    hostRate   = 0.20           # Fraction that get hospitalized
    healthyTime= 14             # Time after infection that person is healthy and no longer infectious
    nDays      = 1000
    sd         = 100              # Standard deviation for gaussian distribution for infection


    # Initialization
    N = 10**4       # Number of agents
    agentL = []
    for i in range(N):
        agentL.append(AGENT())

    # Make one person infected
    agentL[100].infected = True
    agentL[100].start = 0
    yV = np.zeros([nDays])
    xV = np.asarray(range(nDays))

    # Do simulation.  Run over 100 days. I'm sure I'm screwing up my monte-carlo methods
    for day in range(nDays):
        nInfect = 0
        for agent in agentL:
            if(agent.infected == True):
                nInfect += 1
                diff = day - agent.start
                if(diff > incubTime):
                    idx = int(np.random.normal(loc=i, scale=sd))  #index of possible infection
                    # If random number outside of boundary, ignore
                    if(idx < 0 or idx >=N):
                        continue
                    # prob of infection = R0 / (healthyTime - infectTime
                    prob = R0 / (healthyTime - infectTime)
                    rng = random.random()
                    if(rng < prob and agentL[idx].immune == False):
                        agentL[idx].infected= True
                        agentL[idx].start   = day
                        agent.nInfect += 1
                        nInfect += 1
                if(diff > healthyTime):
                    agent.immune = True 
                    agent.infected = False
        yV[day] = nInfect

    # Get number immune
    nImmune = 0
    for agent in agentL:
        if(agent.immune == True):
            nImmune += 1
                
    print("Number immune == {}".format(nImmune))
    
    fig, ax = plt.subplots(1,1)
    ylabel="Number of infections"
    ax.plot(xV, yV, label=ylabel)
    ax.legend()
    plt.show()



    print("Ended : %s"%(time.strftime("%D:%H:%M:%S")))
    print("Run Time : {:.4f} h".format((time.time() - startTime)/3600.0))



    sys.exit(0)


if __name__ == "__main__":
    main()
