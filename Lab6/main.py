import math
import random
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')



def readFromFile(inputFile = "dataset.csv"):
    dates = dict()
    minX = None
    maxX = None
    minY = None
    maxY = None
    with open(inputFile, "r") as file:
        lines = file.readlines()
        lines = lines[1:]
        for line in lines :
            line = line.strip()
            elements = line.split(',')
            label = elements[0]
            valX = float(elements[1])
            valY = float(elements[2])
            dates[(valX, valY)] = label
            if minX == None :
                minX = valX
                maxX = valX
                minY  = valY
                maxY = valY
            else :
                minX = min(minX, valX)
                maxX = max(maxX, valX)
                minY = min(minY, valY)
                maxY = max(maxY, valY)
    return [dates, minX, maxX, minY, maxY]

def randomCentroids(minX, maxX, minY, maxY, centroids):
    while len(centroids) != 4 :
        valX = round(random.uniform(minX, maxX),2)
        valY = round(random.uniform(minY, maxY),2)
        centroid = (valX, valY)
        centroids.add(centroid)

def distance(centroid, point):
    centroidX = centroid[0]
    centroidY = centroid[1]
    pointX = point[0]
    pointY = point[1]
    return math.sqrt((centroidX-pointX)**2+(centroidY-pointY)**2)

def getClosestCentroid(centroids , point) :
    minDistance = None
    resultCentroid = None
    for centroid in centroids :
        currentDist = distance(centroid, point)
        if minDistance == None :
            minDistance = currentDist
            resultCentroid = centroid
        else :
            if (currentDist < minDistance) :
                minDistance = currentDist
                resultCentroid = centroid
    return resultCentroid

def kMeans():
    data = readFromFile()
    minX = data[1]
    maxX = data[2]
    minY = data[3]
    maxY = data[4]
    points = data[0]
    centroidsPoints = dict()
    centroids = set()
    randomCentroids(minX, maxX, minY, maxY, centroids)
    stop = False

    while not stop :
        stop = True
        centroidsPoints = dict()
        newCentroids = set()
        for centroid in centroids :
            centroidsPoints[centroid] = list()
        for point in points.keys() :
            closestCentroid = getClosestCentroid(centroids, point)
            label = (points[point])
            pointToAdd = (point[0], point[1], label)
            centroidsPoints[closestCentroid].append(pointToAdd)
        for centroid in centroids :
            numberPoints = len(centroidsPoints[centroid])
            if numberPoints != 0:
                sumX = 0
                sumY = 0
                for point in centroidsPoints[centroid]:
                    sumX += point[0]
                    sumY += point[1]
                newX = round(sumX / numberPoints, 2)
                newY = round(sumY / numberPoints, 2)
                newCentroid = (newX, newY)
                newCentroids.add(newCentroid)
                if newCentroid not in centroids:
                    stop = False
            else :
                stop = False
        if len(newCentroids) != 4 :
            randomCentroids(minX, maxX, minY, maxY, newCentroids)
        centroids = newCentroids

    classes = list()
    for centroid in centroidsPoints.keys() :
        classes.append(centroidsPoints[centroid])
    labeledClasses = dict()
    for oneClass in classes :
        label = assignLabelToClass(oneClass)
        labeledClasses[label] = oneClass
    return labeledClasses


def assignLabelToClass(oneClass) :
    labels = dict()
    labels['A'] = 0
    labels['B'] = 0
    labels['C'] = 0
    labels['D'] = 0
    for point in oneClass :
        labels[point[2]] += 1
    return max(labels, key=labels.get)

def statisticsInput():
    data = readFromFile()
    data = data[0]
    stats = dict()
    labels = ['A', 'B', 'C', 'D']
    for label in labels :
        stats[label] = 0
    for point in data.keys():
        stats[data[point]] += 1
    return stats

def computeStatisticsClassified(classes):
    precision = dict()
    rappel = dict()
    score = dict()
    totalPositiveExamples = statisticsInput()
    totalCorrectClasified = 0
    for label in classes.keys() :
        oneClass = classes[label]
        currentCorrectClasified = 0
        for point in oneClass :
            if point[2] == label :
                currentCorrectClasified += 1
        totalCorrectClasified += currentCorrectClasified
        precisionCurrent = currentCorrectClasified / len(oneClass)
        rappelCurrent = currentCorrectClasified / totalPositiveExamples[label]
        scoreCorrect = 2*precisionCurrent*rappelCurrent/(precisionCurrent + rappelCurrent)
        precision[label] = precisionCurrent
        rappel[label] = rappelCurrent
        score[label] = scoreCorrect
    accuracy = totalCorrectClasified / sum(totalPositiveExamples.values())
    statistics = dict()
    statistics['accuracy'] = accuracy
    statistics['precision'] = precision
    statistics['rappel'] = rappel
    statistics['score'] = score
    return statistics



if __name__=='__main__':
    classes = kMeans()
    statistics = computeStatisticsClassified(classes)
    print('\nAccuracy', statistics['accuracy'],'\n')
    labels = ['A', 'B', 'C', 'D']
    for label in labels :
        print("Class "+label+" : \n")
        print(classes[label])
        for point in classes[label] :
            if point[2] != label :
                print(point, end=" ")
        print('\n')
        print("\nClass "+label+" statistics :")
        print("precision "+str(statistics['precision'][label]))
        print("rappel " + str(statistics['rappel'][label]))
        print("score " + str(statistics['score'][label]))
        print('\n')
    colors = ["red", "blue", "green", "orange"]
    for i in range(len(labels)) :
        oneClass = classes[labels[i]]
        color = colors[i]
        for point in oneClass :
            plt.scatter(point[0], point[1], color = color, s=30)
    plt.show()
