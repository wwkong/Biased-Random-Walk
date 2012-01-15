# Random Walk Simulation
# By William Kong
# November 26, 2011

# Based on Lectures 17 to 19 of the MIT Intro to Comp. Sci. and Prog. Series
# by Prof. Eric Grimson and Jogn Guttag

# Here, I will be creating a 2-dimensional random walk simulator, starting with a basic 
# stochastic model with a unifrom distribution and move towards various other distributions

# CLASSES ----------------------------------------------------------------------

import math, pylab, random

# Here, we define a couple classes:

# --- Location ---
# DESCRIPTION: represents a location on the co-ordinate plane
# FIELDS: Nat(x), Nat(y)

class Location(object):
    def __init__(self,x,y):
        self.x = float(x)
        self.y = float(y)
    def move(self, xc, yc):
        return Location(self.x+float(xc), self.y+float(yc))
    def getCoords(self):
        return self.x, self.y
    def getDist(self, other):
        ox, oy = other.getCoords()
        xDist = self.x - ox
        yDist = self.y -oy
        return math.sqrt(xDist**2 + yDist**2)
    
# --- CompassPt ---
# DESCRIPTION: This class will detail how an object will move across the plane 
#              using the four cardinal directions, N, W, E, W
# FIELDS: Location(pt)

class CompassPt(object):
    possibles = ('N', 'E', 'S', 'W')  #Re-ordered to adapt to GaussDrunk
    def __init__(self,pt):
        if pt in self.possibles: self.pt = pt
        else: raise ValueError('in CompassPt.__init__')
    def move(self, dist):
        if self.pt == 'N': return (0, dist)
        elif self.pt == 'S': return (0, -dist)
        elif self.pt == 'E': return (dist, 0)
        elif self.pt == 'W': return (-dist, 0)
        else: raise ValueError('in CompassPt.move')
        
# --- Field ---
# DESCRIPTION: Describes the location of a drunk on the plane
# FIELDS: Drunk(drunk), Location(loc)
        
class Field(object):
    def __init__(self, drunk, loc):
        self.drunk = drunk
        self.loc = loc
    def move(self, cp, dist):
        oldLoc = self.loc
        xc, yc = cp.move(dist)
        self.loc = oldLoc.move(xc, yc)
    def getLoc(self):
        return self.loc
    def getDrunk(self):
        return self.drunk
    def isChute(self):
        x, y = self.loc.getCoords()
        return abs(x) - abs(y) == 0
    
# --- oddField ---
# DESCRIPTION: Sub-class of the typical field except now if the drunk passes by 
#              the y=x or y=-x lines, the drunk will return to the origin
# FIELDS: Drunk(drunk), Location(loc); inherits attributes from Field class

class oddField(Field):
    def isChute(self):
        x, y = self.loc.getCoords()
        return abs(x) - abs(y) == 0
    def move(self, cp, dist):
        Field.move(self, cp, dist)
        if self.isChute():
            self.loc = Location(0, 0)
    
# --- Drunk ---
# DESCRIPTION: Creates attributes for the drunk (or person) moving on the plane
# FIELDS: Str(name)

class Drunk(object):
    def __init__(self, name):
        self.name = name
    def move(self, field, cp, dist = 1):
        if field.getDrunk() != self:
            raise ValueError('Drunk.move called with drunk not in field')
        for i in range(dist):
            field.move(cp, 1)
            
# Here begins the different drunk types that will be used to influence the 
# behaviour of the simulation; I will also include some distributions for 
# some of these objects
            
# --- UsualDrunk ---
# DESCRIPTION: Behaves like the usual drunk where the probability of going
#              N, S, E, W per time unit is normally distributed
# Fields: Str(name); inherits attributes from Drunk class

class UsualDrunk(Drunk):
    def move(self, field, dist = 1):
        cp = random.choice(CompassPt.possibles)
        Drunk.move(self, field, CompassPt(cp), dist)
    def __str__(self):
        return 'UsualDrunk travels '

# --- ColdDrunk ---
# DESCRIPTION: If given a cp that is 'S', this Drunk will move twice the distance
#              in that direction; likes warm weather
# Fields: Str(name); inherits attributes from Drunk class

class ColdDrunk(Drunk):
    def move(self, field, dist = 1):
        cp = random.choice(CompassPt.possibles)
        if cp == 'S':
            Drunk.move(self, field, CompassPt(cp), 2*dist)
        else:
            Drunk.move(self, field, CompassPt(cp), dist)
    def __str__(self):
        return 'ColdDrunk travels '
            
# --- EWDrunk ---
# DESCRIPTION: This drunk can only move E or W; analogous to a one dimensional
#              random walk
# Fields: Str(name); inherits attributes from Drunk class

class EWDrunk(Drunk):
    def move(self, field, dist = 1):
        cp = random.choice(CompassPt.possibles)
        while cp != 'E' and cp != 'W':
            cp = random.choice(CompassPt.possibles)
        Drunk.move(self, field, CompassPt(cp), dist)    
    def __str__(self):
        return 'EWDrunk travels '
    
# --- MultiDrunk ---
# DESCRIPTION: This drunk can moves either N, S, E, W under a multinomial distribution
# Fields: Str(name); inherits attributes from Drunk class

class MultiDrunk(Drunk):
    def setProbs(self, pN, pS, pE, pW): # Make sure pN + pS + pE +pW = 1
        self.probN = pN
        self.probS = pS
        self.probE = pE
        self.probW = pW
    def move(self, field, dist = 1):
        num = random.random()
        if 0 <= num <= self.probN:
            cp = 'N'
        elif self.probN  <= num <= (self.probN + self.probS):
            cp = 'S'
        elif (self.probN + self.probS) <= num <= (self.probN + self.probS + self.probE):
            cp = 'E'
        elif (self.probN + self.probS + self.probE) <= num <= 1:
            cp = 'W'
        Drunk.move(self, field, CompassPt(cp), dist) 
        
# --- GaussDrunk ---
# DESCRIPTION: This drunk can moves either N, S, E, W under a gaussian distribution;
#              note that the mean will be centered on one of the cardinals, where
#              that cardinal will be given the 'value' of 0 and cardinals near it
#              will have values ~0; for example, if 'E' is the mean, then 
#              'E' = (-x/2, x), 'N' = [-3x/2,-x/2), 'S' = (x/2,3x/2], 
#              and W = (-infty, -x) U (x, infty) where x will be the spread of 
#              the directional cardinals
# Fields: Str(name); inherits attributes from Drunk class

class GaussDrunk(Drunk):
    def setDirection(self, dr):
        self.direction = dr
    def setProbParam(self, sigma): #sigma = std deviation
        self.mean = 0  # Keep distribution centered at 0 for simplicity
        self.stdD = sigma 
    def setSpread(self, spread):
        self.spread = spread
    def move(self, field, dist = 1):
        center = self.direction
        ctrIndex = CompassPt.possibles.index(center)
        left = CompassPt.possibles[ctrIndex - 1]
        right = CompassPt.possibles[ctrIndex - 3]
        opposite = CompassPt.possibles[ctrIndex - 2]
        
        num = random.gauss(0,self.stdD)
        spread = self.spread
        if -spread/2 <= num <= spread/2:
            cp = center
        elif -3*spread/2 <= num <= -spread/2:
            cp = left
        elif spread/2  <= num <= 3*spread/2:
            cp = right
        else:
            cp = opposite
        Drunk.move(self, field, CompassPt(cp), dist = 1) 