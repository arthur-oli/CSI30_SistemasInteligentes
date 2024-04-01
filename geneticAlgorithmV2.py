from random import random, randint, shuffle, choices
import matplotlib.pyplot as plt


# Calculates euclidian distance between two points
def calculateEuclidianDistance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

# Generates a matrix of distances between every point of a grid, given the array of points
def generateDistanceMatrix(state):
    stateLength = len(state)
    distanceMatrix = [[0 for x in range(stateLength)] for y in range(stateLength)]

    for i in range(stateLength):
        for j in range(stateLength):
            distanceMatrix[j][i] = distanceMatrix[i][j] = calculateEuclidianDistance(
                state[j], state[i]
            )
    return distanceMatrix

# Calculates the total distance of a state, adding the distance between each point
def calculateTspDistance(state):
    totalDistance = 0
    distanceMatrix = generateDistanceMatrix(state)
    for i in range(len(state) - 1):
        totalDistance += distanceMatrix[i + 1][i]

    # Closed loop, add closing distance (distance between last and first point)
    totalDistance += distanceMatrix[0][-1]
    return totalDistance

def generatePossibleState(currentState):
    randomPoint1 = randint(0, len(currentState) - 1)
    randomPoint2 = randint(0, len(currentState) - 1)
    while randomPoint1 == randomPoint2:
        randomPoint1 = randint(0, len(currentState) - 1)
        randomPoint2 = randint(0, len(currentState) - 1)

    possibleState = currentState.copy()
    shuffle(possibleState)
    return possibleState

def generateStartingPopulation(populationSize, numberOfPoints, maxCoordinate):
    points = []
    for _ in range(numberOfPoints):
        points.append((randint(0, maxCoordinate), randint(0, maxCoordinate)))
    
    population = []
    for _ in range(populationSize):
        distance = calculateTspDistance(points)
        population.append((distance, points))
        points = generatePossibleState(points)
    
    return population

def reproduce(parent1, parent2):
    parentLength = len(parent1[1])
    crossoverPoint = randint(1, parentLength)
    parent1cut = parent1[1][0:crossoverPoint]
    parent2cut = [point for point in parent2[1] if point not in parent1cut]
    crossover = parent1cut + parent2cut
    child = (calculateTspDistance(crossover), crossover)
    return child

def geneticAlgorithm(startingPopulation, maxSteps, mutationRate, adaptationThreshold):
    currentStep = 1
    population = startingPopulation
    currentBestState = sorted(startingPopulation)[0][1]
    currentBestStateDistance = sorted(startingPopulation)[0][0]
    totalBestState = currentBestState
    totalBestStateDistance = currentBestStateDistance
    while(currentStep <= maxSteps):
        newPopulation = []
        for _ in range (len(population)):
            parent1 = sorted(choices(population, k = 4))[0]
            parent2 = sorted(choices(population, k = 4))[0]
            child = reproduce(parent1, parent2)
            if random() < mutationRate:
                randomPoint1, randomPoint2 = randint(0, len(child[1]) - 1), randint(0, len(child[1]) - 1)
                child[1][randomPoint1], child[1][randomPoint2] = child[1][randomPoint2], child[1][randomPoint1]

            newPopulation.append(child)
            population = newPopulation
            currentStep += 1
        
        currentBestState = sorted(population)[0][1]
        currentBestStateDistance = sorted(population)[0][0]
        if currentBestStateDistance < adaptationThreshold:
            totalBestState = currentBestState
            print("Ended by adaptation")
            break

        if currentBestStateDistance < totalBestStateDistance:
            totalBestStateDistance = currentBestStateDistance
            totalBestState = currentBestState
            print("Found a better candidate")
    
    if(currentStep == maxSteps + 1):
        print("Ended by stepcount")
    return totalBestState

def main():
    populationSize = 2000
    numberOfPoints = 25
    maxCoordinate = 100
    maxSteps = 200000
    mutationRate = 0.01
    adaptationThreshold = 200

    startingPopulation = generateStartingPopulation(populationSize, numberOfPoints, maxCoordinate)
    bestState = geneticAlgorithm(startingPopulation, maxSteps, mutationRate, adaptationThreshold)
    bestState.append(bestState[0])
    xb, yb = zip(*bestState)
    plt.subplot(1, 5, 3)
    plt.plot(xb, yb)
    plt.scatter(xb, yb, color="black")
    plt.xlabel("X Coordinates")
    plt.ylabel("Y Coordinates")
    plt.title("Best State")
    plt.show()

if __name__ == "__main__":
    main()
