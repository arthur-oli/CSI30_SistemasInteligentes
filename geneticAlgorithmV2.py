from random import randint

def generateStartingPopulation(numberOfStates, numberOfPoints, maxCoordinate):
    points = []
    for _ in range(numberOfPoints):
        points.append(randint(0, maxCoordinate), randint(0, maxCoordinate))
    pop = []
    for _ in range(numberOfStates):
        distance = calculateTspDistance(points)
        pop.append((distance, points))
        points = generatePossibleState(points)
    return sorted(pop)
