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
import datetime
import random
#random.seed(42)


class AGENT:
    """
    Class to define Agent in simuluation
    """
    def __init__(self,ID=None):
        """
        ARGS:
        RETURN:
        DESCRIPTION:
        DEBUG:
        FUTURE:
        """
        self.infected  = False      # Is agent infected?
        self.nInfect   = 0          # Number of people infected by this agent
        self.start     = -1         # Time step agent infected
        self.hospilized= False      # Is hospitalized
        self.tested    = False      # Is agent tested for virus?
        self.immune    = False      # Is agent tested for virus?
        self.dead      = False      # Is Agent dead?
        self.id        = ID
        # Position - 
        x = random.random()
        y = random.random()
        self.posL = [x,y]            # Let's assume a unit box, b/c why not?
        # Velocity - 
        vx = random.uniform(-1,1)/25.0 # Want crossing time to be about 25 steps
        vy = random.uniform(-1,1)/25.0
        self.vL  = [vx, vy]     # Let's assume a unit box, b/c why not?
        self.quarantine = False




class ITALY_DATA:
    """
    Class to define Italy data in simuluation
    """
    def __init__(self, Date=None, HospitalizedWithSymptoms=None, IntensiveCare=None,
                AllHospitalized=None, HomeIsolation=None,
                TotalCurrentlyPositive=None, NewPositive=None,
                DischargedHealed=None, Dead=None, TotalCases=None, Swabs=None):
        """
        ARGS:
        RETURN:
        DESCRIPTION:
        DEBUG:
        FUTURE:
        """
        # Date
        date = Date.split()
        date = date[0].split('-')
        year = int(date[0])
        month= int(date[1])
        day  = int(date[2])
        self.date=datetime.date(year, month, day)
        # Hospitalized With Symptoms == 'ricoverati_con_sintomi'
        self.hospSymp = int(HospitalizedWithSymptoms)
        # Intensive Care == 'terapia_intensiva'
        self.icu = int(IntensiveCare)
        # Total Hospitalized == 'totale_ospedalizzati'
        self.totalHosp = int(AllHospitalized)
        # Home Isolation == 'isolamento_domiciliare'
        self.homeIsol = int(HomeIsolation)
        # Total Currently Positive == 'totale_attualmente_positivi'
        self.totalPos = int(TotalCurrentlyPositive)
        # NewPositive == 'nuovi_attualmente_positivi'
        self.newPos = int(NewPositive)
        # DischargedHealed == 'dimessi_guariti'
        self.discharge = int(DischargedHealed)   # Presumably from the hospital?
        # Dead == 'deceduti'
        self.dead = int(Dead)
        # Total Cases == 'totale_casi'
        self.totalCases = int(TotalCases)
        # Swabs == 'tamponi'
        self.swabs = int(Swabs)


class JOHNS_HOPKINS_DATA:
    """
    Class to define Agent in simuluation
    """
    def __init__(self, Date=None, HospitalizedWithSymptoms=None, IntensiveCare=None,
                AllHospitalized=None, HomeIsolation=None,
                TotalCurrentlyPositive=None, NewPositive=None,
                DischargedHealed=None, Dead=None, TotalCases=None, Swabs=None):
        """
        ARGS:
        RETURN:
        DESCRIPTION:
        DEBUG:
        FUTURE:
        """

