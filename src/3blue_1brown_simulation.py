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
        "python3 ./src/osu_ide_replication_attempt.py \n"
        "      \n"
        "   To Run: \n"
        "   source ~/.local/virtualenvs/python3.7/bin/activate\n")
    sys.exit(ExitCode)


def displacement(Agent1=None, Agent2=None):
    """
    ARGS:
    RETURN:
    DESCRIPTION:
        Gives displacement between two agents.
    DEBUG:
    FUTURE:
    """
    x1=Agent1.posL[0]
    y1=Agent1.posL[1]

    x2=Agent2.posL[0]
    y2=Agent2.posL[1]

    return np.sqrt( (x1-x2)**2 + (y1-y2)**2)



def move_agent(Agent=None, DeltaT=None):
    """
    ARGS:
    RETURN:
    DESCRIPTION:
        Moves agent. Applies implied boundary conditions [0,0,0] -> [1,1,1]
    DEBUG:
    FUTURE:
    """
    x = Agent.vL[0] * DeltaT + Agent.posL[0]
    y = Agent.vL[1] * DeltaT + Agent.posL[1]

    if(x < 0):
        x = -1.0 * x
        Agent.vL[0] = -1.0 * Agent.vL[0]
    if(y < 0):
        y = -1.0 * y
        Agent.vL[1] = -1.0 * Agent.vL[1]
    if(x > 1.0):
        d = x - 1.0
        x = x - d
        Agent.vL[0] = -1.0 * Agent.vL[0]
    if(y > 1.0):
        d = y - 1.0
        y = y - d
        Agent.vL[1] = -1.0 * Agent.vL[1]
    # Adjust Position
    Agent.posL[0] = x
    Agent.posL[1] = y
    # Adjust velocity
    dvx = random.uniform(-1,1)/100.0 # Want crossing time to be about 25 steps
    dvy = random.uniform(-1,1)/100.0
    Agent.posL[0] += dvx
    Agent.posL[1] += dvy
    

def main():
    """
    ARGS:
    RETURN:
    DESCRIPTION:
    DEBUG:
    FUTURE:
        1. Add option to fit only a specific section of data.
        2. Make main loop NOT O(N^2). Maybe organize by position on a grid.
    """
    # Check Python version
    nArg = len(sys.argv)
    # Use python 3
    if(sys.version_info[0] != 3):
        exit_with_error("ERROR!!! Use Python 3\n")
    # Get options 
    if(len(sys.argv) > 1 and "-h" in sys.argv[1]):
        print_help(0)
    elif(nArg != 1):
        print_help(1)

    startTime = time.time()
    print("{} \n".format(sys.argv),flush=True)
    print("   Start Time : {}".format(time.strftime("%a, %d %b %Y %H:%M:%S ",
                                       time.localtime())),flush=True)
    N     = 100             # Number of Agents
    nDays = 100             # number of days in simulation
    dt    = 0.25            # number of steps in a day, total steps = nDays / dt
    nStep = int(nDays / dt)
    infectTime = 14 / dt    # Infection time in units of steps
    asymptomaticTime = 5 / dt    # Infection time in units of steps
    prob  = 0.25            # Probability of infecting agent within infectDist
    infectDist = 0.15       # Distance person must be within to get infected
    agentL= []

    # Initialize agents
    for n in range(N):
        agent = AGENT(n)
        agentL.append(agent)

    # Infect 1 agent
    agentL[0].infected=True


    # Simulation - O(N**2)
    for step in range(nStep):
        # Use plotting
        sxL = []    # Susceptible xL
        syL = []
        ixL = []    # Infected xL
        iyL = []
        rxL = []    # Removed xL
        ryL = []

        for i in range(len(agentL)):
            agent = agentL[i]
            # Move
            move_agent(agent,dt)
            # Generate for plot
            #xL.append(agent.posL[0])
            #yL.append(agent.posL[1])
            # Susceptible
            if(agent.infected == False and agent.immune == False):
                sxL.append(agent.posL[0])
                syL.append(agent.posL[1])
            # Infected
            if(agent.infected == True):
                ixL.append(agent.posL[0])
                iyL.append(agent.posL[1])
            # Removed
            if(agent.immune == True):
                rxL.append(agent.posL[0])
                ryL.append(agent.posL[1])

            # Susceptible Group - Check if infected
            if(agent.infected == False and (step - agent.start < asymptomaticTime)):
                continue

            # Infectious Group - Try to infect someone
            for j in range(len(agentL)):
                # Skip self
                if(i==j or agentL[j].immune == True or agentL[j].infected == True):
                    continue
                d = displacement(agent, agentL[j])
                if(d <= infectDist):
                    rng = random.uniform(0,1)
                    if(rng < prob):
                        agentL[j].infected=True
                        agentL[j].start = step

             # 'Removed' Group. If survived, adjust time. 
            if(step - agent.start > infectTime):
                agent.infected = False
                agent.immune = True

        # Plot
        fig, ax = plt.subplots()
        ax.scatter(sxL, syL, c="black", marker=".", label="Susceptible")
        ax.scatter(ixL, iyL, c="red",   marker="^", label="Infected")
        ax.scatter(rxL, ryL, c="blue",  marker="s", label="Removed")
        ax.grid(True)
        #ax.legend([".", "^", "s"], ["Removed","Infected","Susceptible"], loc="best")
        ax.legend(loc=1)
        ax.set_xlim((0,1))
        ax.set_ylim((0,1))
        ax.set_title("{:<.2f} days".format(step*dt))
        #plt.show()
        plt.savefig("output/{:04d}.png".format(step))
        plt.close('all')






if __name__ == "__main__":
    main()
