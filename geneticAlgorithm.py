from random import randint, random, choices
import matplotlib.pyplot as plt

point = tuple[float, float]
population = tuple[float, list[point]]

# Calculates euclidian distance between two points
def calculateEuclidianDistance(p1: point, p2: point):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def generatePossibleState(currentState):
    randomPoint1 = randint(0, len(currentState) - 1)
    randomPoint2 = randint(0, len(currentState) - 1)
    while randomPoint1 == randomPoint2:
        randomPoint1 = randint(0, len(currentState) - 1)
        randomPoint2 = randint(0, len(currentState) - 1)
    possibleState = currentState.copy()
    possibleState[randomPoint1], possibleState[randomPoint2] = (
        possibleState[randomPoint2],
        possibleState[randomPoint1],
    )
    # possibleState.append(possibleState[0])
    return possibleState

# Generates "numberOfPoints" random points in a maxCoordinate X maxCoordinate grid
def generateStartingPopulation(
    numberOfStates: int, numberOfPoints: int, maxCoordinate: int
) -> list[population]:
    points = []
    for _ in range(numberOfPoints):
        points.append(
        (float(randint(0, maxCoordinate)), float(randint(0, maxCoordinate)))
    )
    pop = []
    for _ in range(numberOfStates):
        distance = calculateTspDistance(points)
        pop.append((distance, points))
        points = generatePossibleState(points)
    return sorted(pop)

# Generates a matrix of distances between every point of a grid, given the array of points
def generateDistanceMatrix(state: list[point]) -> list[list[int]]:
    stateLength = len(state)
    distanceMatrix = [[0 for x in range(stateLength)] for y in range(stateLength)]

    for i in range(stateLength):
        for j in range(stateLength):
            distanceMatrix[j][i] = distanceMatrix[i][j] = calculateEuclidianDistance(
                state[j], state[i]
            )

    return distanceMatrix


def calculateTspDistance(state: list[point]) -> float:
    totalDistance = 0
    distanceMatrix = generateDistanceMatrix(state)
    for i in range(len(state) - 1):
        totalDistance += distanceMatrix[i + 1][i]

    # Closed loop, add closing distance (distance between last and first point)
    totalDistance += distanceMatrix[0][-1]
    return totalDistance


def pick_best_of_sample(population: list[population], sample_size=4):
    my_choices = choices(population, k=sample_size)
    my_choices_sorted = sorted(my_choices)
    return my_choices_sorted[0]


def geneticAlgorithm(
    startingPopulation: list[population],
    numberOfPoints: int,
    numberOfStatesPicked: int,
    mutationRate: float,
    crossoverRate: float,
    maxSteps: int,
) -> population:
    currentStep = 1
    TARGET = 1000
    currentPopulation: list[population] = startingPopulation
    bestStateFound = currentPopulation[0][1]
    bestDistanceFound = currentPopulation[0][0]
    for i in range(maxSteps):
        possiblePopulation: list[population] = []
        # Choose the 2 best states based on distance
        possiblePopulation.append(currentPopulation[0])
        possiblePopulation.append(currentPopulation[1])
        for i in range(len(currentPopulation)):
            if random() < crossoverRate:
                # Crossover happened
                parent1 = pick_best_of_sample(
                    possiblePopulation, sample_size=numberOfStatesPicked
                )
                parent2 = pick_best_of_sample(
                    possiblePopulation, sample_size=numberOfStatesPicked
                )
                crossoverPoint = int(numberOfPoints / 2)
                child1 = parent1[1][0:crossoverPoint]
                child1.append(parent2[1])

                child2 = parent2[1][0:crossoverPoint]
                child2.append(parent1[1])
            else:
                # Crossover didn't happen
                child1 = choices(possiblePopulation)[0][1]
                child2 = choices(possiblePopulation)[0][1]
                if random() < mutationRate:
                    # Mutation happened
                    # SWAP (mutation)
                    crossoverPoint1 = randint(0, numberOfPoints - 1)
                    crossoverPoint2 = randint(0, numberOfPoints - 1)
                    child1[crossoverPoint1], child1[crossoverPoint2] = (
                        child1[crossoverPoint2],
                        child1[crossoverPoint1]
                    )

                    # SWAP (mutation)
                    crossoverPoint1 = randint(0, numberOfPoints - 1)
                    crossoverPoint2 = randint(0, numberOfPoints - 1)
                    child2[crossoverPoint1], child2[crossoverPoint2] = (
                        child2[crossoverPoint2],
                        child2[crossoverPoint1]
                    )

                possiblePopulation.append((calculateTspDistance(child1), child1))
                possiblePopulation.append((calculateTspDistance(child2), child2))
            currentPopulation = possiblePopulation
            currentStep += 1
            if sorted(currentPopulation)[0][0] < bestDistanceFound:
                print("Estado melhor encontrado")
                bestDistanceFound = currentPopulation[0][0]
                bestStateFound = currentPopulation[0][1]
            
            if sorted(currentPopulation)[0][0] < TARGET:
                print("Distância ótima encontrada")
                bestStateFound = currentPopulation[0][1]
                break

    #bestStateFound = sorted(currentPopulation)[0]
    return bestStateFound


def main():
    # Initial values
    numberOfStates = 2000
    numberOfPoints = 15
    pointMaxCoordinate = 100

    maxSteps = 25000

    # Number of states picked from initial population
    numberOfStatesPicked = 4

    # Must be between 0 and 1
    mutationRate = 0.1
    crossoverRate = 1
    startingPopulation = generateStartingPopulation(
        numberOfStates, numberOfPoints, pointMaxCoordinate
    )
    #bestDist, 
    bestState = geneticAlgorithm(
        startingPopulation,
        numberOfPoints,
        numberOfStatesPicked,
        mutationRate,
        crossoverRate,
        maxSteps,
    )

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
