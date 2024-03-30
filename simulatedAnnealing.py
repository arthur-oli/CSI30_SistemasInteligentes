from random import randint, random, shuffle
from math import cos, sin, pi, exp
import matplotlib.pyplot as plt

# Calcula distância euclidiana entre dois pontos
def euclidDistance (p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

# Gera o início
def generateStartingPoints (numberOfPoints, maxCoordinate):
    pontos = []

    for i in range (numberOfPoints):
        pontos.append((randint(0, maxCoordinate), randint(0, maxCoordinate)))

    return pontos

def generateDistanceMatrix (state):
    stateLength = len(state)
    distanceMatrix = [[0 for x in range(stateLength)] for y in range(stateLength)]

    for i in range(stateLength):
        for j in range(stateLength):
            distanceMatrix[j][i] = distanceMatrix[i][j] = euclidDistance(state[j], state[i])    
    
    return distanceMatrix

def generatePossibleState(currentState):
    randomPoint1 = randint(0, len(currentState) - 1)
    randomPoint2 = randint(0, len(currentState) - 1)
    while (randomPoint1 == randomPoint2):
        randomPoint1 = randint(0, len(currentState) - 1)
        randomPoint2 = randint(0, len(currentState) - 1)
    possibleState = currentState.copy()
    possibleState[randomPoint1], possibleState[randomPoint2] = possibleState[randomPoint2], possibleState[randomPoint1]
    #
    #possibleState.append(possibleState[0])
    return possibleState

def calculateTspDistance(state):
    totalDistance = 0
    distanceMatrix = generateDistanceMatrix(state)
    for i in range (len(state) - 1):
        totalDistance += distanceMatrix[i+1][i]
    
    # Closed loop, add closing distance
    totalDistance += distanceMatrix[0][-1]
    return totalDistance

def simulatedAnnealing(startingState, maxTemperature, minTemperature, startingTotalDistance, maxSteps):
    currentTemperature = 0
    currentStep = 1
    currentState = startingState
    currentTotalDistance = startingTotalDistance
    temperatureSchedule = maxTemperature
    bestTotalDistance = startingTotalDistance
    bestState = startingState
    while(temperatureSchedule >= minTemperature and temperatureSchedule > 0 and currentStep <= maxSteps):
        print(temperatureSchedule, minTemperature)
        currentTemperature += 1
        possibleState = generatePossibleState(currentState)
        possibleStateTotalDistance = calculateTspDistance(possibleState)
        deltaDistance = possibleStateTotalDistance - currentTotalDistance

        if possibleStateTotalDistance < bestTotalDistance:
            bestTotalDistance = possibleStateTotalDistance
            bestState = possibleState.copy()

        elif random() < safe_exp(-deltaDistance / temperatureSchedule):
            currentTotalDistance = possibleStateTotalDistance
            currentState = possibleState.copy()

        temperatureSchedule = minTemperature + (maxTemperature - minTemperature) * ((maxSteps - currentStep)/maxSteps)
        currentStep += 1
    
    return bestState

def safe_exp(x):
    try: return exp(x)
    except: return 0

def generateCircle():
    n_pts = 10
    dr = (2 * pi) / n_pts

    x0 = []
    for i in range(0,n_pts):
        radians = dr * i  
        x0.append([cos(radians), sin(radians)])
    
    shuffle(x0)
    return x0

def main(): 
    numberOfPoints = 25
    pointMaxCoordinate = 100
    maxTemperature = 10.0
    minTemperature = 0.001
    maxSteps = 10000

    #startingState = generateCircle()
    startingState = generateStartingPoints(numberOfPoints, pointMaxCoordinate)
    startingTotalDistance = calculateTspDistance(startingState)
    bestStateSimulatedAnnealing = simulatedAnnealing(startingState, maxTemperature, minTemperature, startingTotalDistance, maxSteps)
    
    startingState.append(startingState[0])
    xs, ys = zip(*startingState)
    plt.subplot(1, 3, 1)
    plt.scatter(xs, ys, color = 'black')
    plt.xlabel('X Coordinates')
    plt.ylabel('Y Coordinates')
    plt.title("Generated Points")

    plt.subplot(1, 3, 2)
    plt.plot(xs, ys)
    plt.scatter(xs, ys, color = 'black')
    plt.xlabel('X Coordinates')
    plt.ylabel('Y Coordinates')
    plt.title("Random Starting State")
    
    bestStateSimulatedAnnealing.append(bestStateSimulatedAnnealing[0])
    xb, yb = zip(*bestStateSimulatedAnnealing)
    plt.subplot(1, 3, 3)
    plt.plot(xb, yb)
    plt.scatter(xb, yb, color = 'black')
    plt.xlabel('X Coordinates')
    plt.ylabel('Y Coordinates')
    plt.title("Best State")

    plt.show()

if __name__ == "__main__":
    main()