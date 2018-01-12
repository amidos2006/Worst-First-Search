import chess
import Global
import random as rnd
import math

class Node:
    def __init__(self, board, parent):
        self.parent = parent;
        self.children = {};
        self.totValue = 0;
        self.nVisits = 0;
        self.board = board;
        self.moves = [];
        for mv in board.legal_moves:
            self.moves.append(mv);
            self.children[mv] = None;

    def expand(self):
        for mv in self.moves:
            if self.children[mv] == None:
                tempBoard = chess.Board(self.board.fen())
                tempBoard.push(mv)
                return self.expandMove(tempBoard, mv)
        return self

    def expandMove(self, board, move):
        newNode = Node(board, self)
        self.children[move] = newNode
        return newNode

    def select(self, depressed, agentTurn):
        bestMv = self.moves[0]
        bestValue = self.children[bestMv].getUCBValue(depressed, agentTurn) + Global.TINY_NUM * rnd.random()
        for mv in self.children:
            child = self.children[mv]
            currentValue = child.getUCBValue(depressed, agentTurn) + Global.TINY_NUM * rnd.random()
            if bestValue < currentValue:
                bestMv = mv;
                bestValue = currentValue

        # if self.parent == None:
        #     print("#############################")
        #     print("Agent Turn: " + str(agentTurn) + " Depressed: " + str(depressed) + " CurrentTurn: " + str(self.board.turn))
        #     print("Visits:")
        #     print([str(mv) + ": " + str(self.children[mv].nVisits) for mv in self.children])
        #     print("TotalValue:")
        #     print([str(mv) + ": " + str(self.children[mv].totValue) for mv in self.children])
        #     print("UCB:")
        #     print([str(mv) + ": " + str(round(self.children[mv].getUCBValue(depressed, agentTurn), 3)) for mv in self.children])
        #     print("Best Move: " + str(bestMv));
        return self.children[bestMv];

    def isFullyExpanded(self):
        for mv in self.children:
            if self.children[mv] == None:
                return False
        return True

    def getUCBValue(self, depressed, agentTurn):
        condition = (not depressed) & (not (agentTurn ^ self.parent.board.turn))
        # print("AgentTurn: " + str(agentTurn) + " Current Turn: " + str(self.parent.board.turn) + " Depressed: " + str(depressed) + " Results: " + str(condition))
        if condition:
            return self.totValue / (self.nVisits + Global.TINY_NUM) + Global.CONSTANT * math.sqrt(self.parent.nVisits/(self.nVisits + Global.TINY_NUM))
        else:
            return -self.totValue / (self.nVisits + Global.TINY_NUM) + Global.CONSTANT * math.sqrt(self.parent.nVisits/(self.nVisits + Global.TINY_NUM))

    def backpropagate(self, value):
        currentNode = self
        while not (currentNode == None):
            currentNode.nVisits += 1;
            currentNode.totValue += value;
            currentNode = currentNode.parent

    def rollout(self):
        board = chess.Board(self.board.fen())
        for i in range(0, Global.ROLLOUT):
            if board.is_game_over():
                break
            moves = list(board.legal_moves)
            board.push(moves[rnd.randint(0,len(moves)-1)])
        return board

class MCTS:
    def __init__(self, depressed, iterationalFlip):
        self.root = None
        self.depressed = depressed
        self.iterationalFlip = iterationalFlip

    def treePolicy(self):
        currentNode = self.root;
        while not currentNode.board.is_game_over():
            if not currentNode.isFullyExpanded():
                currentNode = currentNode.expand()
                break
            currentNode = currentNode.select(self.depressed, self.root.board.turn)
        return currentNode;

    def getMostVisited(self):
        mostVisited = self.root.moves[0]
        for mv in self.root.children:
            if self.root.children[mv].nVisits > self.root.children[mostVisited].nVisits:
                mostVisited = mv
            elif self.root.children[mv].nVisits == self.root.children[mostVisited].nVisits and rnd.random() > 0.5:
                mostVisited = mv
        if Global.VERBOSE:
            print([str(mv) + ": " + str(self.root.children[mv].nVisits) for mv in self.root.children])
            print([str(mv) + ": " + str(self.root.children[mv].totValue) for mv in self.root.children])
        return mostVisited

    def getLeastVisited(self):
        leastVisited = self.root.moves[0]
        for mv in self.root.children:
            if self.root.children[mv].nVisits < self.root.children[leastVisited].nVisits:
                leastVisited = mv
            elif self.root.children[mv].nVisits == self.root.children[leastVisited].nVisits and rnd.random() > 0.5:
                leastVisited = mv

        if Global.VERBOSE:
            print([str(mv) + ": " + str(self.root.children[mv].nVisits) for mv in self.root.children])
            print([str(mv) + ": " + str(self.root.children[mv].totValue) for mv in self.root.children])
        return leastVisited

    def getHighestValue(self):
        highValue = self.root.moves[0]
        for mv in self.root.children:
            if self.root.children[mv].totValue > self.root.children[highValue].totValue:
                highValue = mv
            elif self.root.children[mv].totValue == self.root.children[highValue].totValue and rnd.random() > 0.5:
                highValue = mv
        if Global.VERBOSE:
            print([str(mv) + ": " + str(self.root.children[mv].nVisits) for mv in self.root.children])
            print([str(mv) + ": " + str(self.root.children[mv].totValue) for mv in self.root.children])
        return highValue

    def getHighUCB(self):
        highValue = self.root.moves[0]
        for mv in self.root.children:
            if self.root.children[mv].getUCBValue() > self.root.children[highValue].getUCBValue():
                highValue = mv
        if Global.VERBOSE:
            print([str(mv) + ": " + str(self.root.children[mv].nVisits) for mv in self.root.children])
            print([str(mv) + ": " + str(self.root.children[mv].totValue) for mv in self.root.children])
        return highValue

    def getAction(self, board):
        self.root = Node(chess.Board(board.fen()), None)
        
        for i in range(0, Global.MAX_ITERS):
            newNode = self.treePolicy()
            tempBoard = newNode.rollout()
            newNode.backpropagate(Global.HEURISTIC(tempBoard, board.turn) - Global.HEURISTIC(board, board.turn))
            if self.iterationalFlip:
                self.depressed = not self.depressed

        if Global.BEST_PICK:
            return self.getHighestValue()
        if self.depressed:
                return self.getLeastVisited()
        return self.getMostVisited()

class NormalMCTS(MCTS):
    def __init__(self):
        MCTS.__init__(self, False, False)

class DepMCTS(MCTS):
    def __init__(self):
        MCTS.__init__(self, True, False)

class DepUnDepMCTS(MCTS):
    def __init__(self, percentage):
        MCTS.__init__(self, False, False)
        self.percentage = percentage

    def getAction(self, board):
        self.depressed = False
        if(rnd.random() < self.percentage):
            self.depressed = True
        return MCTS.getAction(self, board)

class SimulatedMCTS(DepUnDepMCTS):
    def __init__(self, rate):
        DepUnDepMCTS.__init__(self, 1)
        self.rate = rate

    def getAction(self, board):
        action = DepUnDepMCTS.getAction(self, board)
        self.percentage *= self.rate
        return action

class FlippingMCTS(MCTS):
    def __init__(self):
        MCTS.__init__(self, True, True)

    def getAction(self, board):
        self.depressed = True
        return MCTS.getAction(self, board)
