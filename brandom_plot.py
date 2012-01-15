# By William Kong
# November 27, 2011

# Based on Lectures 17 to 19 of the MIT Intro to Comp. Sci. and Prog. Series
# by Prof. Eric Grimson and Jogn Guttag

# Here, I will be creating a 2-dimensional random walk simulator, starting with a basic 
# stochastic model with a unifrom distribution and move towards various other distributions

# GLOBAL VARIABLES -------------------------------------------------------------

simNumTime = 500
simNumTrials = 500

UsualTitle = '2D Random Walk Simulation in '+str(simNumTrials)+' Trials '
EWTitle = '1D Random Walk Simulation in '+str(simNumTrials)+' Trials '
ColdTitle = 'Biased (South) Random Walk Simulation in '+str(simNumTrials)+' Trials '
MultiTitle = 'MultiDrunk Simulation in '+str(simNumTrials)+' Trials '
GaussTitle = 'GaussDrunk Simulation in '+str(simNumTrials)+' Trials '

oddUsualTitle = 'Odd ' + UsualTitle

# PLOT -------------------------------------------------------------------------

# Here is where I excute pylab functions to aggregate and plot the results;
# initial conditions are also specified here

# First, import the necessary libraries:

import math, pylab, random
from brandom_classes import *
from brandom_simulator import *

# --- plotTrial ---
# PURPOSE: plots a graph representing how distance from origin changes 
#          over time on n trials which span a set time
# FUNCTION: Nat + Nat + drunkType + fieldType + Str -> (Void)
# NOTE: drunkType is a class from the collection of drunk classes (example of 
#       polymorphism used here)

def plotTrial(time, n, drunkType, fieldType, title):
    drunk = drunkType('UWDrunk')
    pylab.figure() 
    for i in range(n):
        f = fieldType(drunk, Location(0,0))
        distances, locs = performTrial(time,f)
        pylab.plot(distances)
        pylab.xlabel('Time')
        pylab.ylabel('Distance from Origin')
        pylab.title(title) 
    
# --- plotSim ---
# PURPOSE: aggregates the data and plots the analysis of n trials 
#          over a set time
# FUNCTION: Nat + Nat + drunkType + fieldType + Str + simName -> (Void)

def plotSim(maxTime, numTrials, drunkType, fieldType, title, simName):
    means = []
    sim = simName(maxTime, numTrials, drunkType, fieldType)
    distLists, locLists = sim.runSim()
    for t in range(maxTime + 1):
        tot = 0.0
        for distL in distLists:
            tot += distL[t]
        means.append(tot/len(distLists))   
        
    pylab.figure()                             # Distance-Time graph
    pylab.plot(means)
    pylab.ylabel('Distance')
    pylab.xlabel('Time')
    pylab.title(title + '(Avg. Dist.)')
    #pylab.grid(True)
    
    pylab.figure()                             # Scatter Plot
    lastX = []
    lastY = []
    for locList in locLists:
        x, y = locList[-1].getCoords()
        lastX.append(x)
        lastY.append(y)
    pylab.scatter(lastX, lastY)
    
# ---------- OPTIONAL LINE PLOTS -------------    
    
    lb = min(min(lastX),min(lastY)) #lower bound of x values
    ub = max(max(lastX),max(lastY)) #upper bound of x values
    bound = max(abs(lb),abs(ub)) #highest absolute value
    
    #pylab.plot([-bound,bound], [-bound,bound], 'r--')  #Plot the equation y = x
    #pylab.text(bound-7, bound, '$y = x$')
    #pylab.plot([-bound,bound], [bound,-bound], 'r--')  #Plot the equation y = -x 
    #pylab.text(bound-7, -bound, '$y = -x$')
    
    pylab.ylabel('NS Distance')
    pylab.xlabel('EW Distance')
    pylab.title(title + '(Final Locations)')
    pylab.grid(True)

# --------------------------------------------      
    
    #pylab.figure()                             # Histogram of x-coords
    #pylab.hist(lastX)
    #pylab.ylabel('EW Distance')
    #pylab.xlabel('Number of hits')
    #pylab.title(title + '(Distribution of EW Values)')
    
    pylab.figure()                             # Histogram of y-coords
    pylab.hist(lastY)
    pylab.ylabel('NS Distance')
    pylab.xlabel('Number of hits')
    pylab.title(title + '(Distribution of NS Values)')
    
    if drunkType == UsualDrunk: # Print the type 
        print 'UsualDrunk travelled:' 
    elif drunkType == ColdDrunk: 
        print 'ColdDrunk travelled:'
    elif drunkType == EWDrunk: 
        print 'EWDrunk travelled:' 
    print means[maxTime] # Exit the .svg to show the simulated expected distance

# Run the simulations on specified parameters:

# Run simulations on a normal field:
#plotSim(simNumTime, simNumTrials, UsualDrunk, Field, UsualTitle, performSim)
plotSim(simNumTime, simNumTrials, ColdDrunk, Field, ColdTitle, performSim)
#plotSim(simNumTime, simNumTrials, EWDrunk, Field, EWTitle, performSim)

# Run simulations on an 'odd' field:
#plotSim(simNumTime, simNumTrials, UsualDrunk, oddField, oddUsualTitle, performSim)
#plotSim(simNumTime, simNumTrials, ColdDrunk, oddField, ColdTitle, performSim)
#plotSim(simNumTime, simNumTrials, EWDrunk, oddField, EWTitle, performSim)


# --------------- Here is where I made some modifications ---------------------

# First, I will try the new simulator adapted to the MultiDrunk class:
#plotSim(simNumTime, simNumTrials, MultiDrunk, Field, MultiTitle, performMSim)
#plotSim(simNumTime, simNumTrials, MultiDrunk, oddField, MultiTitle, performMSim)

# Global values in brandom_simulator can be manipulated to test the simularities between
# MultiDrunk and other Drunks under certain conditions

# Next is the GaussDrunk class:
#plotSim(simNumTime, simNumTrials, GaussDrunk, Field, GaussTitle, performGSim)
#plotSim(simNumTime, simNumTrials, GaussDrunk, oddField, GaussTitle, performGSim)

pylab.show() # Show the results