# Nick Jones written for CS 361 Intro to Evolutionary Computing; Professor Sherri Goings; March 14, 2011

from gpt import *

def run(crossoverRate, mutationRate, 
        crossoverFunction, mutationFunction, 
        maxTreeDepth, populationSize,
        numGenerations, fileName,
         sample = False):
    """Takes in all the necessary parameters, reads info from file, and runs the GP classifier"""
    rawData, categoryLimits, classToPredict = getDataFromFile(fileName)
    categories = rawData[0].keys() # List of categories
    allData = [] # List of entries
    for dict in rawData:
        allData.append(Entry(dict))
        
    categories.remove(classToPredict) # Only want non-final categories (don't want final prediction category in there)
    
    testEntries = allData
    algo = Algorithm(crossoverRate, mutationRate,
                crossoverFunction, mutationFunction,
                testEntries, allData,
                categories, classToPredict,
                categoryLimits, maxTreeDepth,
                populationSize)
                
    allHeightLists = []
    generationBestFitLists = [] # Each entry is a tuple [genNum, bestFit]
    typeGeneration = 'SteadyState'
                
    for i in range(numGenerations):
        # Run the algorithm
        if typeGeneration == 'SteadyState':
            algo.stepGenerationSteadyState()
        else:
            algo.stepGeneration()
        heights = [x.tree.root.getHeight() for x in algo.population]
        allHeightLists.append(heights)
        topFitness = algo.bestIndividual.fitness
        topFitnessHeight = algo.bestIndividual.tree.root.getHeight()
        generationBestFitLists.append([i, topFitness, topFitnessHeight])
        if i % 50 == 0:
            print 'Generation', algo.generation 
            print 'Best ind\'s fitness:', topFitness
            print 'Best ind\'s height:', topFitnessHeight
            print 'All heights in population:', heights
            print '---------'
        if i % 200 == 0:
            print 'Best ind\'s tree: \n', str(algo.bestIndividual.tree.root)
            
    print 'The best individual found:'
    print 'Fitness:', topFitness
    print 'Height:', topFitnessHeight
    print 'Actual Tree Representation:'
    print algo.bestIndividual.tree.root
        
if __name__ == "__main__":
    # Parameters 
    if len(sys.argv) > 1 and sys.argv[1] != None:
        fileName = sys.argv[1]
    else:
        fileName = 'iris.csv'
    populationSize = 30
    crossoverRate = .8
    mutationRate = .8
    crossoverFunction = unevenSubtreeCrossover
    mutationFunction = mutateAll
    maxTreeDepth = 8
    numGenerations = 500
    numTrials = 1
    
    # Run <numTrials> trials
    for i in range(numTrials):
        run(crossoverRate, mutationRate, 
        crossoverFunction, mutationFunction,
        maxTreeDepth, populationSize,
        numGenerations, fileName,
        sample = False)
        print '---End Trial---'


    