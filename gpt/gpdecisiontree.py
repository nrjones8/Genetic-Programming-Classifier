# Nick Jones written for CS 361 Intro to Evolutionary Computing; Professor Sherri Goings; March 14, 2011

from gpnode import GPNode
from entry import Entry
import random
import copy


class GPDecisionTree(object):
    def __init__(self, allData, categories, classToPredict, categoryLimits, maxDepth = 5, root = None, balanced = False):
        """Takes in parameters, creates an a randomly initialized decision tree"""
        self.root = root
        self.maxDepth = maxDepth 
        self.allData = allData # List of Entry objects
        self.categories = categories # Doesn't include classToPredict
        self.classToPredict = classToPredict
        self.allCategories = categories + [self.classToPredict] # Includes classToPredict
        self.categoryLimits = categoryLimits
        if balanced:
            self.initBalancedTree()
        else:
            self.initUnevenTree()
    
    def initBalancedTree(self):
        """Creates a decision tree of depth <self.depth>"""
        nodesAtCurrentDepth = []
        rootClass = self.pickAnAttribute()
        self.root = GPNode(rootClass, self.pickALimit(rootClass))
        nodesAtCurrentDepth.append(self.root)
        
        depth = 0
        # Initialize tree to one level short of depth
        while depth < self.maxDepth - 2:
            children = []
            for node in nodesAtCurrentDepth:
                children += self.giveChildren(node)
            nodesAtCurrentDepth = children 
            depth += 1
        # Add the last level of nodes, which should be terminating nodes (i.e. the possible predictions)
        self.addTerminatingNodes(nodesAtCurrentDepth)
        
    def initUnevenTree(self):
        """Creates a random decision tree that is not necessarily symmetrical or full"""
        rootClass = self.pickAnAttribute() # Not the classToPredict
        rootValue = self.pickALimit(rootClass)
        self.root = GPNode(rootClass, rootValue)
        nodesNeedingChildren = []
        nodesNeedingChildren.append(self.root)
        depth = 0
        
        while depth < self.maxDepth - 2:
            allChildren = []
            for node in nodesNeedingChildren:
                if node.attribute != self.classToPredict:
                    # Not a terminal node
                    allChildren += self.giveChildren(node, includeClassToPredict = True)
            nodesNeedingChildren = allChildren
            depth += 1
        
        self.removeTerminalNodes(nodesNeedingChildren)
        self.addTerminatingNodes(nodesNeedingChildren)
        
    def removeTerminalNodes(self, listOfNodes):
        """Removes all terminal nodes from <listOfNodes>"""
        nodesToRemove = []
        for x in listOfNodes:
            if x.attribute == self.classToPredict:
                nodesToRemove.append(x)
        for node in nodesToRemove:
            listOfNodes.remove(node)
        
    def giveChildren(self, node, includeClassToPredict = False):
        """Gives children to <node>, returns these children"""
        leftClass = self.pickAnAttribute(includeClassToPredict)
        rightClass = self.pickAnAttribute(includeClassToPredict)
        leftNode = GPNode(leftClass, self.pickALimit(leftClass))
        rightNode = GPNode(rightClass, self.pickALimit(rightClass))
        node.setLeftChild(leftNode)
        node.setRightChild(rightNode)
        return [leftNode, rightNode]
        
    def addTerminatingNodes(self, currentNodes):
        """Adds terminal nodes to all nodes in <currentNodes>"""
        # BE CAREFUL HERE; do I want the final split to have the possibility of predicting the same finalValue?
        terminatingOptions = self.categoryLimits[self.classToPredict]
        for node in currentNodes:
            optionLeft = random.choice(terminatingOptions)
            terminatingOptions.remove(optionLeft)
            optionRight = random.choice(terminatingOptions)
            node.setLeftChild(GPNode(self.classToPredict, optionLeft))
            node.setRightChild(GPNode(self.classToPredict, optionRight))
            terminatingOptions.append(optionLeft)
            
    def pickAnAttribute(self, includeClassToPredict = False):
        """Picks a random attribte (each entry in allData contains every attribute as its keys)"""
        if includeClassToPredict:
            attr = random.choice(self.allCategories)
        else:
            attr = random.choice(self.categories)
        return attr
    
    def pickALimit(self, attribute):
        """Returns a random limit for the given <attribute> from somewhere in its specified values (as maintained by categoryLimits)"""
        possibleLimits = self.categoryLimits[attribute]
        try:
            # Get random number between lower and upper limit 
            limit = random.uniform(possibleLimits[0], possibleLimits[1])
        except TypeError:
            # possibleLimits actually has strings, so <attribute> is categorical; return a random choice from the possibleLimits
            limit = random.choice(possibleLimits)
        return limit
    
    def notTerminatingNode(self, node):
        """Determines whether or not <node> is a terminating node"""
        if node.attribute == self.classToPredict:
            return False
        else:
            return True
        
    def evaluate(self, entries):
        """Tests all entries on his decision tree, returns the number classified correctly, and total entries attempted"""
        correct = 0
        total = len(entries)
        for ent in entries:
            if self.root.evaluate(ent):
                correct += 1
        return correct, total
        
    def __str__(self):
        """Root has everything stored"""
        return str(self.root)
        