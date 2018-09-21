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
        def value(state, agentIndex,depth):
            # # # print('===============Value called by ========================')
            ## # print('agentIndex ', agentIndex,' depth ', depth)
            if self.depth*numAgents == depth:
                ## print('returning terminal state', self.evaluationFunction(state))
                return (self.evaluationFunction(state), Directions.STOP)
            if state.isWin() or state.isLose():
                return (self.evaluationFunction(state), Directions.STOP)
            if agentIndex == 0: return maxValue(state,agentIndex,depth)
            if agentIndex != 0: return minValue(state,agentIndex,depth)

        def maxValue(gameState,agentIndex,depth):
            # print('==============in max agent', agentIndex, 'depth',depth, '=========================')
            v = -99999
            chosen_move = Directions.STOP
            legalMoves = gameState.getLegalActions()
            newAgentIndex = (agentIndex + 1)%numAgents
            for move in legalMoves:
                successor_value, candidate_move = value(gameState.generateSuccessor(agentIndex,move),newAgentIndex,
                                                        depth+1)
                v = max(v, successor_value)
                if v == successor_value:
                    chosen_move = move
            return (v,chosen_move)

        def minValue(gameState,agentIndex,depth):
            # print('===============in min agent', agentIndex, 'depth', depth, '========================')
            v = 99999
            chosen_move = Directions.STOP
            legalMoves = gameState.getLegalActions(agentIndex)
            newAgentIndex = (agentIndex + 1) % numAgents
            for move in legalMoves:
                successor_value, candidate_move = value(gameState.generateSuccessor(agentIndex,move),newAgentIndex,
                                                        depth+1)
                v = min(v, successor_value)
                if v == successor_value:
                    chosen_move = move
            return (v,chosen_move)

        v,chosenMove = value(gameState,0,0)
        return chosenMove

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        def value(state, agentIndex,depth,alpha, beta):
            if self.depth*numAgents == depth:
                return (self.evaluationFunction(state), Directions.STOP)
            if state.isWin() or state.isLose():
                return (self.evaluationFunction(state), Directions.STOP)
            if agentIndex == 0: return maxValue(state,agentIndex,depth,alpha,beta)
            if agentIndex != 0: return minValue(state,agentIndex,depth,alpha,beta)

        def maxValue(gameState,agentIndex,depth, alpha, beta):
            # print('==============in max agent', agentIndex, 'depth',depth, '=========================')
            v = -99999
            chosen_move = Directions.STOP
            legalMoves = gameState.getLegalActions()
            newAgentIndex = (agentIndex + 1)%numAgents
            for move in legalMoves:
                successor_value, candidate_move = value(gameState.generateSuccessor(agentIndex,move),newAgentIndex,
                                                            depth+1, alpha, beta)
                v = max(v, successor_value)
                if v == successor_value:
                    chosen_move = move
                # print('current value of beta is', beta)
                if v > beta:
                    # print("PRUNING maximizer")
                    return (v,chosen_move)
                alpha = max(alpha,v)
                # print('new value of alpha is', alpha)
            ## print('for','maxAgent',agentIndex,'depth',depth,'value is',v, '\n', chosen_successor)
            return (v,chosen_move)

        def minValue(gameState,agentIndex,depth,alpha,beta):
            # print('===============in min agent', agentIndex, 'depth', depth, '========================')
            v = 99999
            chosen_move = Directions.STOP
            legalMoves = gameState.getLegalActions(agentIndex)
            ## print('legalMoves for',agentIndex,'are ', legalMoves)
            newAgentIndex = (agentIndex + 1) % numAgents
            for move in legalMoves:
                successor_value, candidate_move = value(gameState.generateSuccessor(agentIndex,move),newAgentIndex,
                                                            depth+1, alpha, beta)
                v = min(v, successor_value)
                if v == successor_value:
                    chosen_move = move
                # print('current value of alpha is', alpha)
                if v < alpha:
                    # print("PRUNING minimizer")
                    return (v,chosen_move)
                beta = min(beta, v)
                # print('new value of beta is', beta)
            ## print('for','minAgent',agentIndex,'depth',depth,'value is',v, '\n', chosen_successor)
            return (v,chosen_move)

        v,chosenMove = value(gameState,0,0, -999, 999)
        return chosenMove


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
        numAgents = gameState.getNumAgents()
        def value(state, agentIndex,depth):
            # # print('===============Value called by ========================')
            ## print('agentIndex ', agentIndex,' depth ', depth)
            if self.depth*numAgents == depth:
                ## print('returning terminal state', self.evaluationFunction(state))
                return (self.evaluationFunction(state), Directions.STOP)
            if state.isWin() or state.isLose():
                return (self.evaluationFunction(state), Directions.STOP)
            if agentIndex == 0: return maxValue(state,agentIndex,depth)
            if agentIndex != 0: return expValue(state,agentIndex,depth)

        def maxValue(gameState,agentIndex,depth):
            # print('==============in max agent', agentIndex, 'depth',depth, '=========================')
            v = -99999
            chosen_move = Directions.STOP
            legalMoves = gameState.getLegalActions()
            newAgentIndex = (agentIndex + 1)%numAgents
            for move in legalMoves:
                successor_value, candidate_move = value(gameState.generateSuccessor(agentIndex,move),newAgentIndex,
                                                        depth+1)
                v = max(v, successor_value)
                if v == successor_value:
                    chosen_move = move
            return (v,chosen_move)

        def expValue(gameState,agentIndex,depth):
            # print('===============in exp agent', agentIndex, 'depth', depth, '========================')
            v = 0
            chosen_move = Directions.STOP
            legalMoves = gameState.getLegalActions(agentIndex)
            newAgentIndex = (agentIndex + 1) % numAgents
            for move in legalMoves:
                prob = 1.0/len(legalMoves)
                successor_value, candidateMove = value(gameState.generateSuccessor(agentIndex,move), newAgentIndex,
                                                       depth+1)
                # get probability
                successor_value *= prob
                v += successor_value
            random_number = random.randint(0,len(legalMoves)-1)
            # # print('random number is', random_number)
            # # print('number of exp agents is', len(expAgentStates))
            chosen_move = legalMoves[random_number]
            ## print('for','minAgent',agentIndex,'depth',depth,'value is',v, '\n', chosen_successor)
            return (v,chosen_move)


        # Generate successor states from legalmoves
        # for each successor state
        v,chosenMove = value(gameState,0,0)
        return chosenMove


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    foodlist = sorted(newFood.asList(), key=lambda t: t[1])
    foodDistances = [manhattanDistance(i, newPos) for i in foodlist]
    minFood = min(foodDistances, default=0)
    ghostDistances = [(manhattanDistance(i, newPos), c) for c, i in enumerate(successorGameState.getGhostPositions())]
    nearestGhost = min(ghostDistances, default=0, key=lambda t: t[0])

    if nearestGhost[0] < 2:
        return -999999
    if newScaredTimes[0] > 5:
        return (nearestGhost[0] * (newScaredTimes[nearestGhost[1]]) * 5
                - minFood * 50 - successorGameState.getNumFood() * 500)
    else:
        return (nearestGhost[0] * (newScaredTimes[nearestGhost[1]] ) *5
                - minFood * 5 - successorGameState.getNumFood() * 500)

    ### better version
    
    # tempScore = currentGameState.getScore()
    # if minFood != 0:
    #     tempScore +=  1 /(minFood+1)
    # if newScaredTimes[0] > 5:
    #     tempScore += 20/(minFood+1)
    #
    # return tempScore


# Abbreviation
better = betterEvaluationFunction
