# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 18:27:55 2018

@author: user
"""

import random
import math
import matplotlib.pyplot as plt
from statistics import mean, stdev

def trainingProgram1(launch_count):
    """
    linear function modeling probability of successful bottle flip.
    It is based on information from Alexandre: after two years of training
    (approx. 100 launch per day), he is able to do two bottle flips every three launches.
    ie bottleProb becomes 2/3 after approx. 100,000 launches (2 years) of training.  
    launch_count an int > 0 (cumulative number of launches)
    returns a number between 0 nd 1, new probability of successful bottle flip.
    """
    if (2/3)/10**5*launch_count >= 1:
        return 1
    return (2/3)/10**5*launch_count

def trainingProgram2(launch_count):
    """
    logarithm function modeling probability of successful bottle flip.
    It is based on information from Alexandre: after two years of training
    (approx. 100 launch per day), he is able to do two bottle flips every three launches.
    ie bottleProb becomes 2/3 after approx. 100,000 launches (2 years) of training.  
    launch_count an int > 0 (cumulative number of launches)
    returns a number between 0 nd 1, new probability of successful bottle flip.
    """
    if launch_count == 0:
        return 0
    if math.log(launch_count, 10**(15/2)) >= 1:
        return 1
    return math.log(launch_count, 10**(15/2))

def launchesToGoal(trainingFunction, goal):
    """
    simulates n launches until goal of consecutive bottle flips is achieved
    trainingFunction, a function which provides probability of successful bottle flip,
    based on the cumulative number of launches.
    returns cumulative number of launches needed to achieve goal
    """
    launch_count, best_seq, current_seq, bottleProb = 0, 0, 0, 0
    while best_seq < goal:
        # random launch of the bottle
        if random.random() <= bottleProb: # successful launch
            current_seq += 1
        else:
            current_seq = 0
        launch_count += 1 # update launch count
        bottleProb = trainingFunction(launch_count) # update probability of successful bottle flip
#        print(current_seq, launch_count, bottleProb)
        if current_seq > best_seq: # check if current sequence beats best sequence
            best_seq = current_seq
    return launch_count

def simulationBottleFlips(trainingFunction, goal, numTrials):
    """
    """
    result = []
    for numTrial in range(numTrials):
        result.append(launchesToGoal(trainingFunction, goal))
    return result

def plotResults(trainingFunction, goal, numTrials):
    import matplotlib.pyplot as plt
    x = simulationBottleFlips(trainingFunction, goal, numTrials)
    num_bins = numTrials/10
    n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
    plt.show()

#plotResults(trainingProgram1, 10, 100)

test = simulationBottleFlips(trainingProgram1, 10, numTrials = 10000)
print(mean(test), round(stdev(test),1))
n, bins, patches = plt.hist(test, 100, facecolor='blue', alpha=0.5)
