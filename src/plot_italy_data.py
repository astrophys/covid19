# Author : Ali Snedden
# Date   : 3/21/20
# License: MIT
# Purpose: 
#   This code plots the Italian Department of Civil Protection Covid-19 Data
#   
#
#   
# Notes : 
#  
# Future:
#   
#
#
import sys
import numpy as np
import time
from matplotlib import pyplot as plt
from error import exit_with_error
from classes import ITALY_DATA
from scipy import optimize


def print_help(ExitCode):
    """
    ARGS:
    RETURN:
    DESCRIPTION:
    DEBUG:
    FUTURE:
    """
    sys.stderr.write(
        "python3 ./src/plot_italy_data.py option_to_plot italy_data_file [log-lin] [index]\n"
        "      option_to_plot : \n"
        "           'hosp_w_sympt'  : Hospitalized w/ Symptoms\n"
        "           'icu'           : Intensive Care Units\n"
        "           'total_hosp'    : All Hospitalized\n"
        "           'home_isolation': Home Isolation \n"
        "           'total_positive': All Positive\n"
        "           'new_positive'  : New Positive\n"
        "           'discharged'    : Discharged\n"
        "           'dead'          : Dead\n"
        "           'total_cases'   : Total Cases\n"
        "           'swabs'         : Swabs\n"
        "      italy_data_file : the path to the dpc-covid19-ita-andamento-nazionale.csv\n"
        "      [log-lin]     : optional, plot y axis in natural log, if straight line \n"
        "                      then experiencing exponential growth. If not specified, \n"
        "                      linear assumed\n"
        "      [slice_index] : optional, for fitting, e.g. \n"
        "                      if = -10, it will fit the last 10 points\n"
        "                      if = 10, it will fit the first 10 points\n"
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
    elif(nArg != 3 and nArg != 4 and nArg != 5):
        print_help(1)
    if(nArg >= 4 and sys.argv[3] == "log-lin"):
        plotType = "log-lin"       # Straight line equals exponential growth
    elif(nArg >= 4 and sys.argv[3] == "lin-lin"):
        plotType = "lin-lin"
        #exit_with_error("ERROR!! Invalid option for plottype, not yet implemented\n")
    else:
        plotType = "log-lin"       # Straight line equals linear growth
    if(nArg == 5):
        slcIdx = int(sys.argv[4])
    else :
        slcIdx = 0

    startTime = time.time()
    print("{} \n".format(sys.argv),flush=True)
    print("   Start Time : {}".format(time.strftime("%a, %d %b %Y %H:%M:%S ",
                                       time.localtime())),flush=True)
    
    # Get args
    option   = sys.argv[1]
    dataPath = sys.argv[2]
    dataFile = open(dataPath, "r")
    italyDataL = []

    # Read csv file
    for line in dataFile:
        line = line.split(',')
        if(line[0] == 'data'):
            continue
        date        = line[0]
        country     = line[1]
        hosp_w_symp = line[2]
        icu         = line[3]
        totalHosp   = line[4]
        homeIsolation = line[5]
        totalPositive = line[6]
        newPositive = line[7]
        discharged  = line[8]
        dead        = line[9]
        totalCases  = line[10]
        swabs       = line[11]
        italyData = ITALY_DATA(Date=date, HospitalizedWithSymptoms=hosp_w_symp,
                               IntensiveCare=icu, AllHospitalized=totalHosp,
                               HomeIsolation=homeIsolation,
                               TotalCurrentlyPositive=totalPositive,
                               NewPositive=newPositive, DischargedHealed=discharged,
                               Dead=dead, TotalCases=totalCases, Swabs=swabs)
        italyDataL.append(italyData)

    # Get values to plot
    n  = len(italyDataL)
    xV = np.asarray([x for x in range(n)])
    yV = np.zeros([n])
    i  = 0
    for italyData in italyDataL:
        if(option == 'hosp_w_sympt'):
            yV = np.asarray([y.hospSym for y in italyDataL])
            ylabel = "Hospitalized with Symptoms"

        elif(option == 'icu'):
            yV = np.asarray([y.icu for y in italyDataL])
            ylabel = "ICU"

        elif(option == 'total_hosp'):
            yV = np.asarray([y.totalHosp for y in italyDataL])
            ylabel = "Total Hospilized"

        elif(option == 'home_isolation'):
            yV = np.asarray([y.homeIsol for y in italyDataL])
            ylabel = "Home Isolation"

        elif(option == 'total_positive'):
            yV = np.asarray([y.totalPos for y in italyDataL])
            ylabel = "Total Positive"

        elif(option == 'new_positive'):
            yV = np.asarray([y.newPos for y in italyDataL])
            ylabel = "New Positive"

        elif(option == 'discharged'):
            yV = np.asarray([y.discharge for y in italyDataL])
            ylabel = "Discharged"

        elif(option == 'dead'):
            yV = np.asarray([y.dead for y in italyDataL])
            ylabel = "Dead"

        elif(option == 'total_cases'):
            yV = np.asarray([y.totalCases for y in italyDataL])
            ylabel = "Total Cases"

        elif(option == 'swabs'):
            yV = np.asarray([y.swabs for y in italyDataL])
            ylabel = "Swabs"

        else:
            exit_with_error("ERROR!!! invalid option ({}) for "
                            "option_to_plot\n".format(option))

    fig, ax = plt.subplots(1,1)
    # Generate Plot
    if(plotType == "log-lin"):
        yV = np.log(yV)
        # Slice and only keep what 
        if(nArg == 5 or nArg == 3):
            if(slcIdx <= 0):
                xfit = xV[slcIdx:]
                yfit = yV[slcIdx:]
            elif(slcIdx > 0):
                xfit = xV[:slcIdx]
                yfit = yV[:slcIdx]
        # Reuse xfit, and yfit
        fit = np.polyfit(xfit,yfit,deg=1)
        xfit= np.asarray([x for x in np.arange(0,n,n/100.0)])
        yfit= fit[0]*xfit + fit[1]
        ax.plot(xfit, yfit, label="Fit - y={:.3f}x+{:.3f}".format(fit[0],fit[1]))
    elif(plotType == "lin-lin"):
        yV = yV
        # Slice and only keep what 
        if(nArg == 5 or nArg == 3):
            if(slcIdx <= 0):
                xfit = xV[slcIdx:]
                yfit = yV[slcIdx:]
            elif(slcIdx > 0):
                xfit = xV[:slcIdx]
                yfit = yV[:slcIdx]
        # Reuse xfit, and yfit
        fit = np.polyfit(xfit,yfit,deg=1)
        xfit= np.asarray([x for x in np.arange(0,n,n/100.0)])
        yfit= fit[0]*xfit + fit[1]
        ax.plot(xfit, yfit, label="Fit - y={:.3f}x+{:.3f}".format(fit[0],fit[1]))
        
    else:
        exit_with_error("ERROR!!! plotType = {} is invalid\n".format(plotType))
    ax.plot(xV, yV, label=ylabel)
    ax.set_title("Time vs. ln({})".format(ylabel))
    ax.set_xlabel("Time")
    ax.set_ylabel("ln({})".format(ylabel))
    ax.legend()
    plt.show()

    print("Ended : %s"%(time.strftime("%D:%H:%M:%S")))
    print("Run Time : {:.4f} h".format((time.time() - startTime)/3600.0))



    sys.exit(0)

if __name__ == "__main__":
    main()
