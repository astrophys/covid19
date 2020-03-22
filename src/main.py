# Author : Ali Snedden
# Date   : 3/16/20
# License: MIT
# Purpose: 
#   
#   
#   
# Notes : 
#  
#  
#   
#
# Future:
#   
#   
#
#
#
import time
import numpy as np
import random as rnd
import sys
import pickle
from error import exit_with_error
from datetime import datetime

def print_help(ExitCode):
    """
    ARGS:
    RETURN:
    DESCRIPTION:
    DEBUG:
    FUTURE:
    """
    sys.stderr.write("python3 ./src/main.py \n"
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
    ## Get options 
    if(sys.version_info[0] == 2 and "-h" in sys.argv[1]):
        print_help(0)
    elif(nArg != 3):
        print_help(1)
    elif(nArg == 3):
        runType=sys.argv[1]
        item = sys.argv[2]
        if(runType != "user" and runType != "hashtag"):
            print_help(1)

    startTime = time.time()
    outDir = "output"
    print("{} \n".format(sys.argv),flush=True)
    print("   Start Time : {}".format(time.strftime("%a, %d %b %Y %H:%M:%S ",
                                       time.localtime())),flush=True)


    sys.exit(0)

if __name__ == "__main__":
    main()
