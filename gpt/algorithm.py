# Nick Jones written for CS 361 Intro to Evolutionary Computing; Professor Sherri Goings; March 14, 2011

from gpdecisiontree import *
from individual import *
from geneticfunctions import *

class Algorithm(object):
    def __init__(self, crossoverRate, mutationRate,
                crossoverFunction, mutationFunction,
                testEntries, allData,
                categories, classToPredict,
                categoryLimits, maxTreeDepth,
                populationSize = 60):
        """<testEntries> will be list of entries that algorithm will test each tree against"""
        # Genetic stuff
        self.crossoverRate = crossoverRate
        self.mutationRate = mutationRate
        self.mutationFunction = mutationFunction
        self.crossoverFunction = crossoverFunction
        self.populationSize = populationSize
        self.population = []
        self.bestIndividual = None
        self.worstIndividual = None
        self.generation = 0
        self.populationSize = populationSize
        # Tree, data etc.
        self.testEntries = testEntries
        self.allData = allData
        self.categories = categories
        self.classToPredict = classToPredict
        self.categoryLimits = categoryLimits
        self.maxTreeDepth = maxTreeDepth
        self.initPopulation(evenDistribution = True)
        
    def initPopulation(self, evenDistribution = False):
        """Initializes population to have <self.populationSize> random individuals (with random decision trees)"""
        if evenDistribution:
            # Trees will be initialized to varying heights 
            increment = self.maxTreeDepth / 4
            heights = [increment, 2*increment, 3*increment, self.maxTreeDepth]
        else:
            heights = [self.maxTreeDepth]*4
        for i in range(self.populationSize):
            fullTree = GPDecisionTree(self.allData, self.categories, self.classToPredict, self.categoryLimits, heights[i%4])
            newInd = Individual(fullTree, fitnessPercentage)
            self.population.append(newInd)
            newInd.updateFitness(self.testEntries)
            
    def stepGeneration(self):
        """Old, slow stepGeneration - no longer used"""
        # Entire population becomes "parents"
        parents = copy.deepcopy(self.population)
        children = copy.deepcopy(parents)
        shuffledChildren = copy.deepcopy(children)
        random.shuffle(shuffledChildren)
        # Crossover children
        for child1, child2 in zip(children, shuffledChildren):
            if random.random() < self.crossoverRate:
                self.crossoverFunction(child1, child2)
                child1.fitness = None
                child2.fitness = None
        # Mutate children
        for child in children:
            if random.random() < self.mutationRate:
                self.mutationFunction(child, self.maxTreeDepth)
                child.fitness = None
        # Reevaluate changed child fitnesses
        for child in children:
            if child.fitness == None:
                # Child has changed - reevaluate fitness
                child.updateFitness(self.testEntries)
                self.totalFitnessEvals += 1
        self.population = []        
        winners = tournamentSelection(parents + children, self.populationSize, self.bestIndividual, tournamentSize = 3) # Always keep the best individual
        for winner in winners:
            self.population.append(winner)
        self.generationPassed()
        
    def stepGenerationSteadyState(self):
        """One step in a steady-state model"""
        parent1 = random.choice(self.population)
        self.population.remove(parent1)
        parent2 = random.choice(self.population)
        self.population.remove(parent2)
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        
        # Crossover and/or mutate children
        if random.random() < self.crossoverRate:
            self.crossoverFunction(child1, child2)
        if random.random() < self.mutationRate:
            self.mutationFunction(child1, self.maxTreeDepth)
        if random.random() < self.mutationRate:
            self.mutationFunction(child2, self.maxTreeDepth)
            
        # Update fitnesses    
        child1.updateFitness(self.testEntries)
        child2.updateFitness(self.testEntries)
        winners = eliteSelection([parent1, parent2, child1, child2], 2)
        self.population += winners
        self.generationPassed()
        
        
    def generationPassed(self):
        """
        Update generation, sort the population.
        """
        self.generation += 1
        self.population.sort(key=lambda i: i.fitness, reverse=True)
        self.bestIndividual = self.population[0]
        self.worstIndividual = self.population[-1]