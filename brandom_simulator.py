# Random Walk Simulation
# By William Kong
# November 28, 2011

# Based on Lectures 19 of the MIT Intro to Comp. Sci. and Prog. Series
# by Prof. Eric Grimson and Jogn Guttag

# Here, I will be creating a 2-dimensional random walk simulator, which will
# contain different behaviours based on the move function defined for each drunk;
# some probability distributions will be used

# GLOBAL VARIABLES -------------------------------------------------------------

# For MultiDrunk
pN = 0.20
pS = 0.40
pE = 0.20
pW = 0.20

# For Gauss Drunk
gDirection = 'S'
spread = 1
sigma = 1

# SIMULATOR --------------------------------------------------------------------

import math, pylab, random
from brandom_classes import *

# Here is where I define the functions/class that run the simulator:

# --- performTrial ---
# PURPOSE: Run a single trial involving a single drunk on a plane
# FUNCTION: Nat + Field -> (listof Float)

def performTrial(time, f):
    start = f.getLoc()
    distances = [0.0]
    locs = [0.0]
    for t in range(1, time + 1):
        f.getDrunk().move(f)
        newLoc =  f.getLoc()
        distance = newLoc.getDist(start)
        distances.append(distance)
        locs.append(newLoc)
    return distances, locs

# The following function is similar to performSim, except it will be used in 
# the analysis of the data in random_walk_plot:


# --- performSim ---
# PURPOSE: calls performTrial some number of times and a list of lists of data
#          pertaining to each drunk
# FIELDS: Nat + Nat + drunkType + fieldType -> (listof (listof float))
# NOTE: drunkType is a class from the collection of drunk classes (example of 
#       polymorphism used here); same can be said of fieldType

class performSim(object):
    def __init__(self, time, numTrials, drunkType, fieldType):
        self.time = time
        self.numTrials = numTrials
        self.drunkType = drunkType
        self.fieldType = fieldType
    def runSim(self):
        distList = []
        locList = []
        for trial in range(self.numTrials):
            d = self.drunkType('Drunk' + str(trial))
            f = self.fieldType(d, Location(0,0))
            distances, locs = performTrial(self.time, f)
            distList.append(distances)
            locList.append(locs)
        return distList, locList

# --- performMSim ---
# PURPOSE: calls performTrial some number of times and a list of lists of data
#          pertaining to each drunk; specifically used for the MultiDrunk
# FIELDS: Nat + Nat + drunkType + fieldType -> (listof (listof float))
# NOTE: drunkType is a class from the collection of drunk classes (example of 
#       polymorphism used here); same can be said of fieldType

class performMSim(performSim):
    def runSim(self):
        distList = []
        locList = []
        for trial in range(self.numTrials):
            d = self.drunkType('Drunk' + str(trial))
            d.setProbs(pN, pS, pE, pW)
            f = self.fieldType(d, Location(0,0))
            distances, locs = performTrial(self.time, f)
            distList.append(distances)
            locList.append(locs)
        return distList, locList

# --- performGSim ---
# PURPOSE: calls performTrial some number of times and a list of lists of data
#          pertaining to each drunk; specifically used for the GaussDrunk
# FIELDS: Nat + Nat + drunkType + fieldType -> (listof (listof float))
# NOTE: drunkType is a class from the collection of drunk classes (example of 
#       polymorphism used here); same can be said of fieldType

class performGSim(performSim):
    def runSim(self):
        distList = []
        locList = []
        for trial in range(self.numTrials):
            d = self.drunkType('Drunk' + str(trial))
            f = self.fieldType(d, Location(0,0))
            d.setDirection(gDirection)
            d.setProbParam(sigma)
            d.setSpread(spread)
            distances, locs = performTrial(self.time, f)
            distList.append(distances)
            locList.append(locs)
        return distList, locList