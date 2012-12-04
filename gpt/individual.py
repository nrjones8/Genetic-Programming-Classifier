# Nick Jones written for CS 361 Intro to Evolutionary Computing; Professor Sherri Goings; March 14, 2011

class Individual(object):
    """A simple individual class that contains a GPDecisionTree has its data"""
    def __init__(self, tree, fitnessFunction):
        self.tree = tree
        self.fitnessFunction = fitnessFunction
        self.fitness = None
        
    def updateFitness(self, entries):
        self.fitness = self.fitnessFunction(self, entries)