# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent, Actions

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        foodlist = sorted(newFood.asList(), key=lambda t: t[1])
        foodDistances = [manhattanDistance(i, newPos) for i in foodlist]
        minFood = min(foodDistances, default=0)
        ghostDistances = [(manhattanDistance(i, newPos), c) for c, i in enumerate(successorGameState.getGhostPositions())]
        nearestGhost = min(ghostDistances, default=0, key=lambda t: t[0])

        if action == 'Stop' or nearestGhost[0] < 2:
            return -9999999
        else:
            return nearestGhost[0] * (newScaredTimes[nearestGhost[1]] + 1) - minFood * 5 - successorGameState.getNumFood() * 100

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        print('===============GetAction========================')
        def value(state, agentIndex,depth):
            #print('===============Value called by ========================')
            #print('agentIndex ', agentIndex,' depth ', depth)
            if depth/numAgents == self.depth:
                #print('returning terminal state', self.evaluationFunction(state))
                return (self.evaluationFunction(state),state)
            if agentIndex == 0: return maxValue(state,agentIndex,depth)
            if agentIndex != 0: return minValue(state,agentIndex,depth)
        def maxValue(gameState,agentIndex,depth):
            print('==============in max agent', agentIndex, 'depth',depth, '=========================')
            v = -999
            chosen_successor = None
            legalMoves = gameState.getLegalActions()
            print('legalMoves are ',legalMoves)
            maxAgentStates = [gameState.generateSuccessor(agentIndex, move) for move in legalMoves]
            newAgentIndex = (agentIndex + 1)%numAgents
            for successor in maxAgentStates:
                successor_value, candidateSuccessor = value(successor,newAgentIndex,depth+1)
                v = max(v, successor_value)
                if v == successor_value: chosen_successor = candidateSuccessor
            print('for','maxAgent',agentIndex,'depth',depth,'value is',v, '\n', chosen_successor)
            return (v,chosen_successor)
        def minValue(gameState,agentIndex,depth):
            print('===============in min agent', agentIndex, 'depth', depth, '========================')
            v = 999
            chosen_successor = None
            legalMoves = gameState.getLegalActions(agentIndex)
            print('legalMoves are ', legalMoves)
            minAgentStates = [gameState.generateSuccessor(agentIndex, move) for move in legalMoves]
            newAgentIndex = (agentIndex + 1) % numAgents
            for successor in minAgentStates:
                successor_value, candidateSuccessor = value(successor, newAgentIndex,depth+1)
                v = min(v, successor_value )
                if v == successor_value: chosen_successor = candidateSuccessor
            print('for','minAgent',agentIndex,'depth',depth,'value is',v, '\n', chosen_successor)
            return (v,chosen_successor)


        # Generate successor states from legalmoves
        # for each successor state
        v, chosenSuccessor = value(gameState,0,0)
        print('============== FINAL ========================')
        print('v is ', v, '\n', chosenSuccessor)
        # legalMoves = gameState.getLegalActions()
        # print(legalMoves)
        # potentialStates = [gameState.generateSuccessor(0, move) for move in legalMoves]
        # print(potentialStates)
        # chosenIndex = [index for index in range(len(legalMoves)) if potentialStates[index] == chosenSuccessor]
        # print('chosenIndex is',chosenIndex)
        # return legalMoves[chosenIndex[0]]
        if chosenSuccessor == None:
            return 'Stop'
        else:
            directionVector = (chosenSuccessor.getPacmanPosition()[0]-gameState.getPacmanPosition()[0],
                               chosenSuccessor.getPacmanPosition()[1] - gameState.getPacmanPosition()[1])
            direction = Actions.vectorToDirection(directionVector)
        return direction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
