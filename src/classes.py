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


class AGENT:
    """
    Class to define Agent in simuluation
    """
    def __init__(self):
        """
        ARGS:
        RETURN:
        DESCRIPTION:
        DEBUG:
        FUTURE:
        """
        self.isInf     = False      # Is agent infected?
        self.nInf      = 0          # Number of people infected by this agent
        self.startInf  = -1         # Time step agent infected
        self.isHosp    = False      # Is hospitalized
        self.isTest    = False      # Is agent tested for virus?
        self.isDead    = False      # Is Agent dead?
