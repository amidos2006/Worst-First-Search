import checkers
import Global
import Agents
import sys
import os.path
import math
import random as rnd

def writeFile(filename, line):
    f = None
    if os.path.isfile(filename):
        f = open(filename, 'a')
    else:
        f = open(filename, 'w')
    f.write(line + "\n")
    f.close()

def playGame(agents):
    board = checkers.CheckerBoard()
    currentTurn = 0
    while not board.is_over():
        agent = agents[currentTurn % 2]
        agentMove = agent.getAction(board.copy())
        board.make_move(agentMove)

        # if VERBOSE:
        print("Turn: " + str(currentTurn))
        print("Current Move: " + str(agentMove))
        print("Current Board:")
        print(board)
        print(Global.HEURISTIC(board, (currentTurn%2)==0))
        print("")

        currentTurn = currentTurn + 1
        if currentTurn > Global.MAX_TURNS:
            return "0 - 0"

    return board.result()

def playAllAgainst(filename, agent, parameter, seed):
    agentName = agent.__class__.__name__
    Agents.fixSeed(seed)
    result = playGame([Agents.NormalMCTS(), agent]).split("-")
    writeFile(filename, "NormalMCTS" + ", " + agentName + ", " + str(parameter) + ", " + result[0] + ", " + result[1])
    Agents.fixSeed(seed)
    result = playGame([agent, Agents.NormalMCTS()]).split("-")
    writeFile(filename, agentName + ", " + "NormalMCTS" + ", " + str(parameter) + ", " + result[0] + ", " + result[1])

# def allEffect(filename):
#     playAllAgainst(filename, Agents.DepMCTS(), "")
#     for i in range(1, 6):
#         percentage = round(1.0 - i / 10.0, 1)
#         rate = round(1.0 - i / 10.0, 1)
#         playAllAgainst(filename, Agents.DepUnDepMCTS(percentage), str(percentage))
#         playAllAgainst(filename, Agents.SimulatedMCTS(rate), str(rate))

def singleEffect(filename, parameter):
    seed = rnd.randint(0, Global.BIG_NUM)
    playAllAgainst(filename, Agents.DepMCTS(), str(parameter), seed)
    playAllAgainst(filename, Agents.DepUnDepMCTS(0.5), str(parameter), seed)
    playAllAgainst(filename, Agents.SimulatedMCTS(0.97), str(parameter), seed)
    playAllAgainst(filename, Agents.FlippingMCTS(), str(parameter), seed)
    playAllAgainst(filename, Agents.NormalMCTS(), str(parameter), seed)

# def iterationsEffect(filename):
#     Global.MAX_ITERS = 1000
#     Global.ROLLOUT = 10
#     Global.CONSTANT = math.sqrt(2)
#     for i in range(5, 11):
#         Global.MAX_ITERS = math.pow(2, i)
#         singleEffect(filename, Global.MAX_ITERS)
#
# def rolloutEffect(filename):
#     Global.MAX_ITERS = 1000
#     Global.ROLLOUT = 10
#     Global.CONSTANT = math.sqrt(2)
#     for i in range(3, 9):
#         Global.ROLLOUT = math.pow(2, i)
#         singleEffect(filename, Global.ROLLOUT)
#
# def constantEffect(filename):
#     Global.MAX_ITERS = 1000
#     Global.ROLLOUT = 10
#     Global.CONSTANT = math.sqrt(2)
#     for i in range(1, 11):
#         Global.CONSTANT = round(i / 5.0, 2)
#         singleEffect(filename, Global.CONSTANT)

def main(argv):
    playerIndex = argv[0]

    Global.BEST_PICK = True
    testIterations = [64, 128, 256]
    testRollouts = [8, 16, 32]
    testHeuristics = [Global.simpleHeuristic]

    filename = "results/results" + playerIndex + ".csv"
    writeFile(filename, "Agent Black, Agent White, Parameter, Black Wins, White Wins")
    while True:
        for i in range(0, len(testIterations)):
            for her in testHeuristics:
                Global.MAX_ITERS = testIterations[i]
                Global.ROLLOUT = testRollouts[i]
                Global.HEURISTIC = her
                singleEffect(filename, str(Global.MAX_ITERS) + "-" + str(Global.ROLLOUT))

if __name__ == "__main__":
   main(sys.argv[1:])
