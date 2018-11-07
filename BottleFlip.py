# -*- coding: utf-8 -*-
"""
Created on Sat May  5 17:02:21 2018

@author: user
"""

#this program simulates bottle flips. it is trying to answer the question:
#how many times do i need to launch a bottle to complete 100 consecutive bottle flips?
#the model assumes a launcher will improve its odds of doing a bottle flip,
#because he gains skill, launch after launch. TrainingProgram object tries to
#replicate this behavior.

class Bottle(object):
    """
    a bottle has one core parameter: its probability to fall on its bottom
    after it has been launched (a bottle flip).
    """
    def __init__(self, flipProb):
        self.flipProb = flipProb
        
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def getFlipProb(self):
        return self.flipProb

class TrainingProgram(object):
    """
    The training program increases bottleProb, up to 1, as much as x, the number of launches grows.
    its core parameter is a function which spits out a new bottle probability,
    based on the cumulative number of launches.
    """
    def __init__(self, bottle, trainingFunction):
        self.bottle = bottle
        self.trainingFunction = trainingFunction
    
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def getBottleFlipProb(self):
        return self.bottle.getFlipProb()
    
    def getTrainedFlipProb(self, x):
        return self.trainingFunction(x, self.bottle.getFlipProb())
    
#    def getTrainedFlipProb(self, x):
#        if (2/3 - self.bottle.getFlipProb())/10**5*x + self.bottle.getFlipProb() >= 1:
#            return 1
#        return (2/3 - self.bottle.getFlipProb())/10**5*x + self.bottle.getFlipProb()

class Launcher(object):
    """
    the boy who launches. His goal is to do x consecutive bottle flips.
    Experience helps him master the art of bottle flips and his odds
    of launching a bottle on its bottom increase according to the trainingProg object.
    """
    def __init__(self, trainingProg, goal):
        self.trainingProg = trainingProg
        self.goal = goal
        self.launches = []
        self.best = (0,0)

    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
        
    def getTrainingProgram(self):
        return self.trainingProg.getName()
        
    def getGoal(self):
        return self.goal
    
    def getLastLaunches(self, x):
        try:
            return self.launches[-x:]
        except:
            IndexError('There are less than ', str(x), ' launches.')
    
    def getAllLaunches(self):
        return self.launches
    
    def getTotalNumLaunches(self):
        return len(self.launches)
    
    def bestPerf(self):
        #this line returns the longest sequence of 1s
        try:
            return max(len(list(y)) for (x,y) in itertools.groupby(self.launches) if x==1)
        except ValueError:
            return 0
    
    def getBestPerf(self):
        """
        returns
        """
        r = max((list(y) for (x,y) in itertools.groupby((enumerate(self.launches)),operator.itemgetter(1)) if x == 1), key=len)
        self.best = (r[0][0], r[-1][0])
        return str('The longest sequence of bottle flips is '+str(self.best[1] - self.best[0] + 1)\
                   +'. You first achieved this result from launch #'\
                   +str(self.best[0]+1)+' to launch #'+str(self.best[1]+1)+'.')
    
    def launch(self):
        if random.random() <= self.trainingProg.getTrainedFlipProb(len(self.launches)):
            self.launches.append(1)
        else:
            self.launches.append(0)
            
def trainingProgram1(x, bottleProb):
    """
    linear function used by the training program objects.
    it is based on information from Alexandre: after two years of training
    (approx. 100 launch per day), he is able to do two bottle flisp every three launches.
    ie bottleProb becomes 2/3 after approx. 100,000 launches (2 years) of training.  
    x an int > 0 (num of launches)
    bottleProb the brobability of the bottle to fall on its bottom.
    returns a new probability, which is a function of x.
    """
    if (2/3 - bottleProb)/10**5*x + bottleProb >= 1:
        return 1
    return (2/3 - bottleProb)/10**5*x + bottleProb

def trainingProgram2(x, bottleProb):
    """
    logarithmic function, with the same logic: 2/15*log10(100,000) = 2/3.
    ie bottleProb becomes 2/3 after approx. 100,000 launches (2 years) of training.  
    x an int > 0 (num of launches)
    bottleProb the probability of the bottle to fall on its bottom.
    returns a new probability, which is a function of x.
    """
    if x == 0 or 2/15*log10(x) <= bottleProb:
        return bottleProb
    if 2/15*log10(x) >= 1:
        return 1
    return lo10(x)

#def trainingProgram3(x, bottleProb):
#    if x <= 100:
#        return 1
#    if log(x,100) >= 1/bottleProb:
#        return 1/bottleProb
#    return log(x,100)

import itertools, operator, math, pylab

def simulationBottleFlips(bottle, trainingFunction, goal, numTrials = 100):
    """
    """
    result = {}
    for numTrial in range(numTrials):
        training = TrainingProgram(bottle, trainingFunction)
        Alexandre = Launcher(training, goal)
        best = 0
        while best < goal:
            Alexandre.launch()
            if Alexandre.getLastLaunches(1) == 1:
                best += 1
            else:
                best = 0
            if best in range(10, goal+1, 10):
                if numTrial == 0:
                    result[best] = []           
                result[best].append(Alexandre.getTotalNumLaunches())
    return result
#    yValues = []
#    xValues = list(result.keys())
#    for i in range(len(xValues)):
#        yValues.append(sum(list(result.values())[i])/numTrials)
#    pylab.plot(xValues, yValues, label = "Linear training")
#    pylab.title("Bottle flip simulation")
#    pylab.xlabel("# of consecutive bottle flips")
#    pylab.ylabel("Average number of launches")
#    pylab.legend(loc = "best")
#    pylab.show()
#    print(Alexandre.getBestPerf())
#    print(Alexandre.getTotalNumLaunches())

import random
simulationBottleFlips(Bottle(0.2), trainingProgram1, 10, numTrials = 1)

#bottle = Bottle(0.2)
#linearTraining = TrainingProgram(bottle, trainingProgram1)
#linearTraining.setName('linearTraining')
#Alexandre = Launcher(linearTraining, 2)
#Alexandre.setName('Alexandre')
##for i in range(37057):
#best = Alexandre.bestPerf()
#while best < 10:
#    Alexandre.launch()
#    best = Alexandre.bestPerf()
##print(Alexandre.getLastLaunches(100))
#print(Alexandre.getBestPerf())
#print(Alexandre.bestPerf())
#print(Alexandre.getTotalNumLaunches())