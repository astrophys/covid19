# Author : Ali Snedden
# Date   : 3/21/20
# License: MIT
# Purpose: 
#   This code plots the Johns Hoptins Covid-19 Data
#   
#
#   
# Notes : 
#   
# References : 
#   1. https://github.com/CSSEGISandData/COVID-19
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
        "python3 ./src/plot_jhu_data.py country [log-lin] [index]\n"
        "      country   : See time_series_covid19_confirmed_global.csv\n"
        "                  for coutries to plot options\n"
        "      \n"
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
    elif(nArg != 4 and nArg != 3):
        print_help(1)
    if(nArg == 4):
        slcIdx = int(sys.argv[3])

    startTime = time.time()
    print("{} \n".format(sys.argv),flush=True)
    print("   Start Time : {}".format(time.strftime("%a, %d %b %Y %H:%M:%S ",
                                       time.localtime())),flush=True)
    
    # Get args
    country = sys.argv[1]
    plotType = sys.argv[2]       # Straight line equals linear growth
    dataPath = "data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    countryFound = False
    df = pd.read_csv(dataPath)
    lastDate = df.columns[-1]
    for index, row in df.iterrows():
        # Select country specified
        if(row.values[1].lower() == country.lower()):
            if(countryFound == True):
                exit_with_error("ERROR!! {} should only occur "
                                "once".format(country.lower()))
            yV = np.asarray(row.values[4:],dtype=np.float32)  # y vector -cases
            xV = np.asarray(range(len(yV)))                   # x vector - days
            n  = len(xV)   # Number of days
            countryFound = True
   
    fig, ax = plt.subplots(1,1)
    # Generate Plot
    if(plotType == "log-lin"):
        ylabel = "ln(cases + 1)"
        print(yV)
        yV = yV + 1
        yV = np.log(yV)
        # Slice and only keep what 
        if(nArg == 4):
            if(slcIdx < 0):
                xfit = xV[slcIdx:]
                yfit = yV[slcIdx:]
            elif(slcIdx > 0):
                xfit = xV[:slcIdx]
                yfit = yV[:slcIdx]
        fit = np.polyfit(xfit,yfit,deg=1)
        # Reuse xfit, and yfit
        xfit= np.asarray([x for x in np.arange(0,n,n/100.0)])
        yfit= fit[0]*xfit + fit[1]
        ax.plot(xfit, yfit, label="Fit - y={:.3f}x+{:.3f}".format(fit[0],fit[1]))
        ax.set_title("Covid-19 in {} (ending {})".format(country, lastDate))
    elif(plotType == "lin-lin"):
        ylabel = "Covid-19_Cases"
        exit_with_error("ERROR!! I haven't handled this option yet\n")
        
    else:
        exit_with_error("ERROR!! Invalid plotType option\n")
    ax.plot(xV, yV, label=ylabel)
    ax.set_xlabel("Time spanning 0-{} days".format(n-1))
    ax.set_ylabel("{}".format(ylabel))
    ax.legend()
    plt.show()

    print("Ended : %s"%(time.strftime("%D:%H:%M:%S")))
    print("Run Time : {:.4f} h".format((time.time() - startTime)/3600.0))



    sys.exit(0)


if __name__ == "__main__":
    main()
