# Nick Jones, written for CS 361 - Intro to Evolutionary Computing with Sherri Goings

from entry import Entry 

class GPNode(object):
    """"""
    def __init__(self, attribute, comparisonValue):
        """
        <attribute> is the attribute this node 'cares about' i.e. what attribute to compare
        <comparisonValue> is either a limit (if numeric) or a category (if categorical)
        """
        self.attribute = attribute
        self.comparisonValue = comparisonValue
        self.attributeType = type(comparisonValue).__name__ # 'str' or 'float'
        self.leftChild = None
        self.rightChild = None
        
    def setLeftChild(self, newNode):
        self.leftChild = newNode
        
    def setRightChild(self, newNode):
        self.rightChild = newNode
        
    def getLeftChild(self):
        return self.leftChild
        
    def getRightChild(self):
        return self.rightChild
        
    def evaluate(self, entry):
        """Determines if this tree (as represented by root node) correctly classifies <entry>"""
        if self.leftChild == None and self.rightChild == None:
            # Terminal node, so compare entry's final category with this node's final category
            return self.comparisonValue == entry.attributes[self.attribute]
        elif self.compareAttributes(entry):
            # Compare; go right if true, left if false
            return self.rightChild.evaluate(entry)
        else:
            return self.leftChild.evaluate(entry)
        
    def compareAttributes(self, entry):
        """
        Compares this node's attribute with the entry's attribute 
        NOTE: Node's limit is always compared to data's limit in form: data's attribute < limit
        """
        if self.attributeType == 'str':
            # Must be a categorical attribute, so compare this node's category with that of the entry
            return self.comparisonValue == entry.attributes[self.attribute]
        else:
            # Must be a numeric attribute
            return self.comparisonValue > entry.attributes[self.attribute]
            
    def getHeight(self):
		"""Returns the height of the tree descending from this node. For example, if the node has no children then returns 0."""
		# Compute the height of the left subtree.
		if self.leftChild == None:
			leftHeight = -1
		else:
			leftHeight = self.leftChild.getHeight()
		# Compute the height of the right subtree.
		if self.rightChild == None:
			rightHeight = -1
		else:
			rightHeight = self.rightChild.getHeight()
		return 1 + max(leftHeight, rightHeight)
            
    def __str__(self):
        """Returns a string representation, with an empty child represented by []. Assumes that the values stored in the tree themselves respond to __str__."""
        # Get the string for the left child.
        if self.leftChild == None:
            leftString = '[]'
        else:
            leftString = str(self.leftChild)
        # Get the string for the right child.
        if self.rightChild == None:
            rightString = '[]'
        else:
            rightString = str(self.rightChild)
        selfString = str(self.attribute)
        if self.attributeType == 'str':
            selfString += ' = ' + self.comparisonValue 
        else:
            selfString += ' > ' + str(self.comparisonValue)
        
        return '[' + selfString + ', ' + leftString + ', ' + rightString + ']'
        
if __name__ == "__main__":
    root = GPNode('height', 4)
    root.setLeftChild(GPNode('weight', 190))
    root.setRightChild(GPNode('size', 12))
    curL = root.getLeftChild()
    curR = root.getRightChild()
    curL.setRightChild(GPNode('height', 10))
    curL.setLeftChild(GPNode('foot', 12))
    curR.setRightChild(GPNode('hand', 9))
    curR.setLeftChild(GPNode('toe', 99))
    print root
    print 'height:', root.getHeight()

            
