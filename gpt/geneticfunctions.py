# Nick Jones written for CS 361 Intro to Evolutionary Computing; Professor Sherri Goings; March 14, 2011
# Contains all genetic functions used by the Algorithm class

from parsedata import getDataFromFile
from entry import Entry
from gpdecisiontree import GPDecisionTree
from gpnode import GPNode
import copy
import random
import sys


def fitnessPercentage(ind, entries):
    """<ind>'s tree is evaluated based on entries, returns percentage correctly classified"""
    correct, total = ind.tree.evaluate(entries)
    return correct / (float(total))
    
def mutateAll(ind, maxDepth):
    """
    Calls deletion mutation automatically if tree too large (1.25 maxDepth)
    Calls random subtree mutation 50% , deletion 25%, adjust comparison value 25%
    """
    if ind.tree.root.getHeight() > maxDepth + maxDepth / 4:
        mutateDeletion(ind)
    rand = random.random()
    if rand > .75:
        mutateDeletion(ind)
    elif rand > .5:
        mutateAdjustComparisonValue(ind, 2)
    else:
        mutateRandomSubtree(ind)
        
def mutateDeletion(ind):
    """Delete a random node in <ind>'s tree; replace it with a terminal node"""
    tree = ind.tree
    terminalOptions = tree.categoryLimits[tree.classToPredict]
    terminalReplacement = GPNode(tree.classToPredict, random.choice(terminalOptions))
    nodeToDelete, parentNode, left = getRandomNode(tree.root, random.randint(0, tree.maxDepth))
    if left:
        parentNode.setLeftChild(terminalReplacement)
        terminalReplacement.setLeftChild(None)
        terminalReplacement.setRightChild(None)
    else:
        parentNode.setRightChild(terminalReplacement)
        terminalReplacement.setLeftChild(None)
        terminalReplacement.setRightChild(None)
        
def mutateAdjustComparisonValue(ind, n = 1):
    """Adjusts n of <ind>'s comparisonValues based on a Gaussian that is 10% of the range"""
    for i in range(n):
        node = getRandomNode(ind.tree.root, ind.tree.maxDepth)[0]
        rangeValues = ind.tree.categoryLimits[node.attribute]
        if node.attributeType == 'str':
            # Categorical, so reassign this node's comparison value to a random value
            node.comparisonValue = random.choice(rangeValues)
        else:
            # Numerical, so adjust its value 
            actualRange = rangeValues[1] - rangeValues[0]
            node.comparisonValue += random.gauss(0, actualRange * .3) # this .1 can certainly change 
    
def mutateRandomSubtree(ind, depth = 4):
    """Picks a random node, generates a random subtree to replace that node's subtree"""
    allData = ind.tree.allData
    categories = ind.tree.categories
    classToPredict = ind.tree.classToPredict
    categoryLimits = ind.tree.categoryLimits
    height = depth 
    
    newFullTree = GPDecisionTree(allData, categories, classToPredict, categoryLimits, 2)
    newNode = newFullTree.root
    nodeToReplace, parent, left = getRandomNode(ind.tree.root, depth)
    if left:
        parent.setLeftChild(newNode)
    else:
        parent.setRightChild(newNode)
    del newFullTree
    
def unevenSubtreeCrossover(ind1, ind2):
    """Crosses over at two randomly selected nodes in ind1 and ind2"""
    depth1 = random.randint(0, ind1.tree.maxDepth)
    depth2 = random.randint(0, ind2.tree.maxDepth)
    nodeToSwap1, parentOf1, left1 = getRandomNode(ind1.tree.root, depth1)
    nodeToSwap2, parentOf2, left2 = getRandomNode(ind2.tree.root, depth2)
    if left1:
        parentOf1.setLeftChild(nodeToSwap2)
    else:
        parentOf1.setRightChild(nodeToSwap2)
    if left2:
        parentOf2.setLeftChild(nodeToSwap1)
    else:
        parentOf2.setRightChild(nodeToSwap1)
    
def getRandomNode(startingNode, maxDepth):
    """
    Returns random node in subtree of <startingNode>, the random node's parent, and
    whether the randomNode was a left or right child; goes only as deep as <maxDepth>
    """
    depth = 0
    currentNode = startingNode
    parentOfCurrent = None
    left = None
    while depth <= maxDepth:
        if currentNode.getLeftChild() == None and currentNode.getRightChild() == None:
            # terminal node
            return currentNode, parentOfCurrent, left 
        elif random.random() > .5:
            parentOfCurrent = currentNode # Current about to change; must update its parent to be it
            left = True
            currentNode = currentNode.getLeftChild()
        else:
            parentOfCurrent = currentNode # Current about to change; must update its parent to be it
            left = False
            currentNode = currentNode.getRightChild()
        depth += 1
    return currentNode, parentOfCurrent, left 
        
def tournamentSelection (population, n, bestIndToKeep = None, tournamentSize=2):
    """Select <n> from <population> by n-way tournament. Keeps <bestIndToKeep> no matter what"""
    winners = []
    if bestIndToKeep != None:
        winners.append(bestIndToKeep)
    while len(winners) < n:
        bestCandidate = random.choice(population)
        for i in range(tournamentSize - 1):
            candidate = random.choice(population)
            if candidate.fitness == bestCandidate.fitness:
                # Same fitness, then compare based on height
                if candidate.tree.root.getHeight() < bestCandidate.tree.root.getHeight():
                    bestCandidate = candidate
            elif candidate.fitness > bestCandidate.fitness:
                bestCandidate = candidate
                
        winner = copy.deepcopy(bestCandidate)
        winners.append(winner)
    return winners
    
def eliteSelection(population, n):
    """Selects the best <n> individuals from <population>"""
    population.sort(key=lambda i: i.fitness, reverse=True)
    return population[:n]