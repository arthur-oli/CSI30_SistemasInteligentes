from random import randint, random, choices
from math import exp, log
import matplotlib.pyplot as plt

# Calculates euclidian distance between two points
def calculateEuclidianDistance (p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

# Generates "numberOfPoints" random points in a maxCoordinate X maxCoordinate grid
def generateStartingPopulation (numberOfStates, numberOfPoints, maxCoordinate):
    population = []
    for i in range (numberOfStates):
        points = []
        for j in range (numberOfPoints):
            points.append((randint(0, maxCoordinate), randint(0, maxCoordinate)))
        
        distance = calculateTspDistance(points)
        population.append([distance, points])
    bestState = sorted(population)[0]
    return population, bestState

# Generates a matrix of distances between every point of a grid, given the array of points
def generateDistanceMatrix (state):
    stateLength = len(state)
    distanceMatrix = [[0 for x in range(stateLength)] for y in range(stateLength)]

    for i in range(stateLength):
        for j in range(stateLength):
            distanceMatrix[j][i] = distanceMatrix[i][j] = calculateEuclidianDistance(state[j], state[i])    
    
    return distanceMatrix

def calculateTspDistance(state):
    totalDistance = 0
    distanceMatrix = generateDistanceMatrix(state)
    for i in range (len(state) - 1):
        totalDistance += distanceMatrix[i+1][i]
    
    # Closed loop, add closing distance (distance between last and first point)
    totalDistance += distanceMatrix[0][-1]
    return totalDistance

def geneticAlgorithm(startingPopulation, numberOfPoints, numberOfStatesPicked, mutationRate, crossoverRate, maxSteps):
    currentStep = 1
    currentPopulation = startingPopulation
    for i in range(maxSteps):
        possiblePopulation = []
        # Choose the 2 best states based on distance
        possiblePopulation.append(sorted(currentPopulation)[0])
        possiblePopulation.append(sorted(currentPopulation)[1])
        for i in range (int((len(currentPopulation) - 2) / 20)):
            if random() < crossoverRate:
                # Crossover happened
                choice1 = choices(possiblePopulation, k = numberOfStatesPicked)
                print(f"{choice1 = }")
                choice2 = choices(possiblePopulation, k = numberOfStatesPicked)
                choice1 = sorted(choice1)
                choice2 = sorted(choice2)
                choice1 = choice1[0]
                choice2 = choice2[0]
                #parent1 = sorted(choices(possiblePopulation, k = numberOfStatesPicked))[0]
                #parent2 = sorted(choices(possiblePopulation, k = numberOfStatesPicked))[0]
                parent1 = choice1
                parent2 = choice2

                crossoverPoint = randint(0, numberOfPoints - 1)
                child1 = parent1[1][0:crossoverPoint]
                for j in parent2[1]:
                    if (j not in child1):
                        child1.append(j)

                child2 = parent2[1][0:crossoverPoint]
                for j in parent1[1]:
                    if (j not in child2):
                        child2.append(j)
            else:
                # Crossover didn't happen
                child1 = choices(possiblePopulation)[0][1]
                child2 = choices(possiblePopulation)[0][1]
                if (random() < mutationRate):
                    # Mutation happened
                    # SWAP (mutation)
                    crossoverPoint1 = randint(0, numberOfPoints - 1)
                    crossoverPoint2 = randint(0, numberOfPoints - 1)
                    child1[crossoverPoint1], child1[crossoverPoint2] = (child1[crossoverPoint2], child1[crossoverPoint1])

                    # SWAP (mutation)
                    crossoverPoint1 = randint(0, numberOfPoints - 1)
                    crossoverPoint2 = randint(0, numberOfPoints - 1)
                    child2[crossoverPoint1], child2[crossoverPoint2] = (child2[crossoverPoint2], child2[crossoverPoint1])
                
                possiblePopulation.append([child1, calculateTspDistance(child1)])
                possiblePopulation.append([child2, calculateTspDistance(child2)])
            currentPopulation = possiblePopulation
            currentStep += 1
                    
    bestStateFound = sorted(currentPopulation)[0]
    return bestStateFound

def main():
    # Initial values
    numberOfStates = 2000
    numberOfPoints = 30
    pointMaxCoordinate = 100
    
    maxSteps = 250
    
    # Number of states picked from initial population
    numberOfStatesPicked = 4

    # Must be between 0 and 1
    mutationRate = 0.1
    crossoverRate = 0.9
    startingPopulation, bestStartingState = generateStartingPopulation(numberOfStates, numberOfPoints, pointMaxCoordinate)
    bestState = geneticAlgorithm(startingPopulation, numberOfPoints, numberOfStatesPicked, mutationRate, crossoverRate, maxSteps)

    #bestState.append(bestState[0])
    xb, yb = zip(*bestState)
    plt.subplot(1, 5, 3)
    plt.plot(xb, yb)
    plt.scatter(xb, yb, color = 'black')
    plt.xlabel('X Coordinates')
    plt.ylabel('Y Coordinates')
    plt.title("Best State")

if __name__ == "__main__":
    main()