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


def print_help(ExitCode):
    """
    ARGS:
    RETURN:
    DESCRIPTION:
    DEBUG:
    FUTURE:
    """
    sys.stderr.write(
        "python3 ./src/plot_italy_data.py option_to_plot italy_data_file\n"
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
    """
    # Check Python version
    nArg = len(sys.argv)
    # Use python 3
    if(sys.version_info[0] != 3):
        exit_with_error("ERROR!!! Use Python 3\n")
    # Get options 
    if("-h" in sys.argv[1]):
        print_help(0)
    elif(nArg != 3):
        print_help(1)
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
    xV = np.zeros([n])
    yV = np.zeros([n])
    i  = 0
    for italyData in italyDataL:
        if(option == 'hosp_w_sympt'):
            
            
        elif(option == 'icu'):

        elif(option == 'total_hosp'):

        elif(option == 'home_isolation'):

        elif(option == 'total_positive'):

        elif(option == 'new_positive'):

        elif(option == 'discharged'):

        elif(option == 'dead'):

        elif(option == 'total_cases'):

        elif(option == 'swabs'):
    
        else:
            exit_with_error("ERROR!!! invalid option ({}) for "
                            "option_to_plot\n".format(option))


    print("Ended : %s"%(time.strftime("%D:%H:%M:%S")))
    print("Run Time : {:.4f} h".format((time.time() - startTime)/3600.0))



    sys.exit(0)

if __name__ == "__main__":
    main()
