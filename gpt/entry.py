# Nick Jones written for CS 361 Intro to Evolutionary Computing; Professor Sherri Goings; March 14, 2011

class Entry(object):
    def __init__(self, attributes):
        """
        <attributes> is a dictionary of form attribute => value, including the final class (to be classified)
        """
        self.attributes = attributes
        
