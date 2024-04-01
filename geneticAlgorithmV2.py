from random import randint

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
    possibleState[randomPoint1], possibleState[randomPoint2] = (possibleState[randomPoint2],possibleState[randomPoint1])
    # possibleState.append(possibleState[0])
    return possibleState

def generateStartingPopulation(populationSize, numberOfPoints, maxCoordinate):
    points = []
    for _ in range(numberOfPoints):
        points.append(randint(0, maxCoordinate), randint(0, maxCoordinate))
    
    population = []
    for _ in range(populationSize):
        distance = calculateTspDistance(points)
        population.append((distance, points))
        points = generatePossibleState(points)
    return population
