# Author : Ali Snedden
# Date   : 4/12/20
# License: MIT
# Purpose: 
#   This code attmpts to follow https://www.youtube.com/watch?v=gxAaO2rsdIs and try to 
#   mimic his plots
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
from matplotlib.patches import Circle
from error import exit_with_error
from scipy import optimize
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
        "python3 ./src/osu_ide_replication_attempt.py [quarentine]\n"
        "   [quarentine] : optional, puts infected in quarentine 2 days after symptoms  \n"
        "      \n"
        "      \n"
        "   After running, create a movie via : "
        "       ffmpeg -framerate 4 -pattern_type glob -i 'tmp/*.png' -c:v libx264 out.mp4\n"
        "      \n"
        "   To Run: \n"
        "       source ~/.local/virtualenvs/python3.7/bin/activate\n")
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
    if(type(Agent1) == AGENT):
        x1=Agent1.posL[0]
        y1=Agent1.posL[1]
    elif(type(Agent1) == list):
        x1=Agent1[0]
        y1=Agent1[1]
    else:
        exit_with_error("ERROR!!! {} not a supported type\n".format(type(Agent1)))
        
    if(type(Agent2) == AGENT):
        x2=Agent2.posL[0]
        y2=Agent2.posL[1]
    elif(type(Agent2) == list):
        x2=Agent2[0]
        y2=Agent2[1]
    else:
        exit_with_error("ERROR!!! {} not a supported type\n".format(type(Agent2)))

    return np.sqrt( (x1-x2)**2 + (y1-y2)**2)



def move_agent(Agent=None, AgentL=None, InfectDist=None, Quarentine=None, DeltaT=None):
    """
    ARGS:
    RETURN:
    DESCRIPTION:
        Moves agent. Applies implied boundary conditions [0,0,0] -> [1,1,1]
    DEBUG:
    FUTURE:
    """
    xi= Agent.posL[0]
    yi= Agent.posL[1]
    vx= Agent.vL[0]
    vy= Agent.vL[1]
    v = np.sqrt(vx**2 + vy**2)
    xf= Agent.vL[0] * DeltaT + Agent.posL[0]
    yf= Agent.vL[1] * DeltaT + Agent.posL[1]
    r = InfectDist      # Radius about quarantined individual

    # Check if quarentined agent nearby.
    #   1. Only consider 1st quarantine encountered b/c it could be potentially very
    #      challenging to solve for preventing a susceptible from completely avoiding _all_
    #      quarantined agents.
    #   2. 
    #   3. 
    #
    if(Quarentine == True):
        avoidInfect = False
        while(avoidInfect == False):
            # displacement, Agent final - initial
            dfi = np.sqrt((xf-xi)**2 + (yf-yi)**2)
            # Get line function,     y = mx + b
            m   = (yf-yi)/(xf-xi)  # Slope of line
            b   = yf - m*xf        # Pick a point on the line, solve for intercept

            for agent in AgentL:
                # Must be quarentined to avoid
                if(agent.quarentine == False):
                    continue
                xc = agent.posL[0]
                yc = agent.posL[1]
                # displ, quarntined - Agent initial
                dfq = np.sqrt((xc-xf)**2 + (yc-yf)**2)
                # displ, quarntined - Agent final 
                diq = np.sqrt((xc-xi)**2 + (yc-yi)**2)
                # There might be a collision.
                if(dfq <= r + dfi or diq <= r + dfi):
                    # Get circle of exclusion line, recall 
                    #   0 = (x - xc)^2 + (y - yc)^2 - r^2
                    #   xc,yc = x,yposition of center of circle
                    def f(x):
                        y = m*x+b
                        return( (x-xc)**2 + (y-yc)**2 - r**2)
                    # Is there a root or crossing?  f(a) * f(b) = -1
                    if( f(xc-r) * f(xc+r) < 0):
                        xroots = optimize.fsolve(f, [xc-r, xc+r])
                        # If there are two roots, which do i pick? Pick closest to Agent
                        if(len(xroots) == 2):
                            x1=xroots[0]
                            y1=f(x1)
                            d1=displacement(Agent,[x1,y1])
                            x2=xroots[1]
                            y2=f(x2)
                            d2=displacement(Agent,[x2,y2])
                            # Use 1st root b/c it is closer
                            if(d1<d2):
                                x=x1
                                y=y1
                            else:
                                x=x2
                                y=y2
                                
                        elif(len(xroots) == 1):
                            x = xroot
                            y =f(x)
                        else:
                            exit_with_error("ERROR!!! I don't understand how there can "
                                            "be more than 2 roots!\n")
                        rvect = [x-xc, y-yc]
                        if(np.isclose(np.sqrt(rvect*rvect), r) == False):
                            exit_with_error("ERROR!!! I don't know how |rvect| != |r|\n")

                        # Now get angle between rvector and velocity vector
                        theta = np.arccos( (vx*rvect[0] + vy*rvect[1]) /
                                           ((vx**2 + vy**2)*(rvect[0]**2 + rvect[1]**2)))
                        # Angle of reflection w/r/t to the tangent line on circle 
                        phi = np.pi - theta
                        vx = v * np.sin(phi)
                        vy = v * np.cos(phi)
                        xf = vx * DeltaT + xi
                        yf = vy * DeltaT + yi
                        break
                    else: 
                        continue
            avoidInfect = True
    else:
        if(xf < 0):
            xf = -1.0 * xf
            Agent.vL[0] = -1.0 * Agent.vL[0]
        if(yf < 0):
            yf = -1.0 * yf
            Agent.vL[1] = -1.0 * Agent.vL[1]
        if(xf > 1.0):
            d = xf - 1.0
            xf = xf - d
            Agent.vL[0] = -1.0 * Agent.vL[0]
        if(yf > 1.0):
            d = yf - 1.0
            yf= yf - d
            Agent.vL[1] = -1.0 * Agent.vL[1]
        # Adjust Position
        Agent.posL[0] = xf
        Agent.posL[1] = yf
        # Adjust velocity
        dvx = random.uniform(-1,1)/100.0 # Want crossing time to be about 25 steps
        dvy = random.uniform(-1,1)/100.0
        Agent.posL[0] += dvx
        Agent.posL[1] += dvy
    

def main():
    """
    ARGS:
    RETURN:
        1. Creates images. Turn into moving using ffmpeg, e.g. 
           ffmpeg -framerate 4 -pattern_type glob -i 'output/*.png' -c:v libx264 out.mp4
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
    elif(nArg != 1 and nArg != 2):
        print_help(1)
    elif(nArg == 1):
        quarantine = False
    elif(nArg == 2 and sys.argv[1] == "quarentine"):
        quarantine = True

    startTime = time.time()
    print("{} \n".format(sys.argv),flush=True)
    print("   Start Time : {}".format(time.strftime("%a, %d %b %Y %H:%M:%S ",
                                       time.localtime())),flush=True)
    N     = 100             # Number of Agents
    nDays = 100              # number of days in simulation
    dt    = 0.25            # number of steps in a day, total steps = nDays / dt
    nStep = int(nDays / dt)
    infectTime = 14 / dt    # Infection time in units of steps
    asymptomaticTime = 5 / dt    # Infection time in units of steps
    prob  = 0.25            # Probability of infecting agent within infectDist
    infectDist = 0.05       # Distance person must be within to get infected
    agentL= []
    nSuscL = []             # Number of susceptible per step
    nInfL = []              # Number of infected per step
    nRmL = []               # Number of removed per step

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
        ### Only if quarentining infected individuals
        if(quarentine == True):
            qxL = []    # quarentine
            qyL = []

        for i in range(len(agentL)):
            agent = agentL[i]
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

            ### Only if quarentining infected individuals
            if(quarentine == True):
                if((step - agent.start - asymptomaticTime >= 2)):
                    agent.quarentine = True
                if(agent.quarentine == True):
                    qxL.append(agent.posL[0])
                    qyL.append(agent.posL[1])
                    continue

            # Move
            move_agent(agent,agentL,dt)

            # Susceptible Group - Check if infected
            if(agent.infected == False or (step - agent.start < asymptomaticTime)):
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
                        agent.nInfect += 1

             # 'Removed' Group. If survived, adjust time. 
            if(step - agent.start > infectTime):
                agent.infected = False
                agent.immune = True

        # Plot
        fig, ax = plt.subplots()
        ax.scatter(sxL, syL, c="black", marker=".", label="Susceptible")
        ax.scatter(ixL, iyL, c="red",   marker="^", label="Infected")
        # Add infection radius
        for i in range(len(ixL)):
            circle = Circle((ixL[i], iyL[i]), radius=infectDist)
            circle.set_edgecolor("red")
            circle.set_facecolor("none")
            ax.add_artist(circle)
        ax.scatter(rxL, ryL, c="blue",  marker="s", label="Removed")
        ax.grid(True)
        #ax.legend([".", "^", "s"], ["Removed","Infected","Susceptible"], loc="best")
        ax.legend(loc=1)
        ax.set_xlim((0,1))
        ax.set_ylim((0,1))
        # State R0
        RL = np.asarray([a.nInfect for a in agentL if(a.immune == True)])
        if(np.sum(RL) > 0):
            R = np.mean(RL)
        else:
            R = 0
        ax.set_title("{:<.2f} days, R = {:<.2f}".format(step*dt,R))
        #plt.show()
        plt.savefig("tmp/{:04d}.png".format(step))
        plt.close('all')

        # Record number susceptible, infected and removed
        nSuscL.append(len(sxL))
        nInfL.append(len(ixL))
        nRmL.append(len(rxL))

    
    # Generate plot of SIR vs. Time
    fig, ax = plt.subplots()
    ax.plot(range(nStep), nSuscL, c="black", label="Susceptible")
    ax.plot(range(nStep), nInfL, c="red", label="Infected")
    ax.plot(range(nStep), nRmL, c="blue", label="Removed")
    ax.legend(loc=1)
    ax.xaxis.set_ticks([d*1.0/dt for d in range(nDays) if(d%10 == 0)])
    ax.set_xticklabels([d for d in range(nDays) if(d%10 == 0)])
    ax.set_title("Susceptible-Infected-Removed vs. Time".format(step*dt))
    plt.savefig("tmp/SIR_vs_time.png")
    plt.close('all')



if __name__ == "__main__":
    main()
