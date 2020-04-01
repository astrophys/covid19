# Author : Ali Snedden
# Date   : 3/21/20
# License: MIT
# Purpose: 
#   This code plots the Johns Hoptins Covid-19 Data. It plots a select few 
#   countries on a semi-log plot
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
        "python3 ./src/plot_country_deaths.py \n"
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
        1. Checked adding countries' data, hopefully don't double count
           if france gets more  points in the regions.  CHecked summing
           of China's regions (since there isn't a global value)
           
           E.g. 
           grep -i china data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv  | awk 'BEGIN{FS=","; SUM=0}{SUM+=$66}END{print SUM}'
3274
    FUTURE:
        1. Add option to fit only a specific section of data.
    """
    # Check Python version
    nArg = len(sys.argv)
    # Use python 3
    if(sys.version_info[0] != 3):
        exit_with_error("ERROR!!! Use Python 3\n")
    # Get options 
    if(nArg > 1 and "-h" in sys.argv[1]):
        print_help(0)
    elif(nArg != 1 ):
        print_help(1)

    startTime = time.time()
    print("{} \n".format(sys.argv),flush=True)
    print("   Start Time : {}".format(time.strftime("%a, %d %b %Y %H:%M:%S ",
                                       time.localtime())),flush=True)
    plotType = "log-lin"
    
    # Get args
    dataPath = "data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
    countryL = ["us","spain","italy","china","korea, south","germany","france",
                "canada"]
    df = pd.read_csv(dataPath)
    lastDate = df.columns[-1]
    dataD = dict()      # A dictionary, keys = country, values=np array of deaths
    for country in countryL:
        for index, row in df.iterrows():
            # Select country specified
            if(row.values[1].lower() == country.lower()):
                vector = np.asarray(row.values[4:],dtype=np.float32)
                # Convert nan's to 0's, maybe wrong?
                for i in range(len(vector)):
                    if(np.isnan(vector[i])):
                        vector[i]=0

                # += b/c some countries, i.e. china don't have a single country val
                if(country in dataD.keys()):
                    # Add
                    dataD[country] += vector
                    # Debugging
                    if(country == 'us' and np.isnan(dataD[country][-1])):
                        print("{} {}".format(country,len(dataD[country])))
                    #### FIGURE OUT NAN at end of US ####
                    if(initLen != len(dataD[country])):
                        exit_with_error("ERROR!!! {} != {}\n".format(initLen,
                                        len(dataD[country])))
                else:
                    dataD[country] = vector
                    initLen = len(dataD[country])
                    
    
    # not every country got deaths at the same time. Let's shift the time
    # points to be starting at the first death(s)
    for country in dataD.keys():
        shiftDataL = []
        firstDeath = False
        dataV = dataD[country]

        for d in range(len(dataV)):
            if(dataV[d] > 0):
                dataD[country]=dataV[d:]
                break
   
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
