# Nick Jones written for CS 361 Intro to Evolutionary Computing; Professor Sherri Goings; March 14, 2011
# Script to parse data from .csv file, return important information and data
import sys

def getDataFromFile(fileName):
    """
    Takes in a fileName that should be in .csv format; each line in this .csv corresponds to a single entry
    Returns <allData>, a list of dictionaries where each member is a dictionary of form category => value
    <categoryLimits> is a dictionary of form category => limits where limits are the possible values for a given category,
    if that category is categorical; if it is numeric, the limits are the upper and lower bound (max and min) values found 
    in the file for that category. <classToPredict> is the final cateogory, which our tree is trying to predict. 
    """
    file = open(fileName, 'r')
    categories = file.readline().rsplit(',')
    allData = [] # Will be a list of dictionaries
    categoryRanges = {} # Category => list of all values for that category
    categoricalCategories = [] # Keeps track of which categories are categorical (non-numerical)
    categoryLimits = {} # Category => [minValue, maxValue] if numeric; [class1, class2, ...] if categorical
    
    # Clean up categories, initialize dictionary entries
    for i in range(len(categories)):
        categories[i] = categories[i].strip()
        categoryRanges[categories[i]] = []
        
    tempLine = file.readline()
    while tempLine != "":
        data = tempLine.rsplit(',')
        tempDict = {}
        for cat, datum in zip(categories, data):
            cleanDatum = datum.strip('\n').strip(' ')
            try:
                # Make it numeric if it should be
                cleanDatum = float(cleanDatum)
            except ValueError:
                # It's not numeric, oh well; add category to list of categoricals
                if cat not in categoricalCategories:
                    categoricalCategories.append(cat)
    
            categoryRanges[cat].append(cleanDatum)
            tempDict[cat] = cleanDatum
        allData.append(tempDict)
        tempLine = file.readline()
    # Fill in any missing entries    
    for dict in allData:
        for cat in categories:
            try:
                dict[cat]
            except KeyError:
                dict[cat] = '?'
    # Figure out limits if numerical, figure out classes if categorical
    for cat in categoryRanges:
        if cat not in categoricalCategories:
            # Numerical attribute
            categoryRanges[cat].sort()
            categoryLimits[cat] = [categoryRanges[cat][0], categoryRanges[cat][-1]] 
        else:
            # Categorical attribute
            categoryLimits[cat] = []
            for value in categoryRanges[cat]:
                if value not in categoryLimits[cat]:
                    categoryLimits[cat].append(value)
                    
    # Want to return list of dicts, limits, and classToPredict
    classToPredict = categories[-1]
    
    return allData, categoryLimits, classToPredict
    
if __name__ == "__main__":
    allData, catLimits, classToPredict = getDataFromFile(sys.argv[1])