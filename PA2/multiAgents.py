# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        newFoodAsList = newFood.asList()
        newGhostPositions = successorGameState.getGhostPositions()
        sumOfDistanceToFood = []
        sumOfDistanceToGhost = []
        # print 'new pos:', newPos
        # print 'newFood:', newFoodAsList
        # print  'newScaredTimes', newScaredTimes
        for newGh in newGhostPositions:
            sumOfDistanceToGhost.append(manhattanDistance(newPos, newGh))
        if len(newFoodAsList) > 0:

            for newFd in newFoodAsList:
                sumOfDistanceToFood.append(manhattanDistance(newPos, newFd))

            return successorGameState.getScore() + 10 / min(sumOfDistanceToFood) - (
                30 * (1 / (min(sumOfDistanceToGhost)+.1)))
        else:
            return 99999


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.minValue(gameState.generateSuccessor(0, action), gameState.getNumAgents(), self.depth, 1) for
                  action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


    def minValue(self, gameState, numberOfAgents, depth, startIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        v = 99999999

        if numberOfAgents == 2:
            depth -= 1
            for ac in gameState.getLegalActions(startIndex):
                v = min(v, self.maxValue(gameState.generateSuccessor(startIndex, ac), depth))

            return v

        else:
            # call min
            numberOfAgents -= 1
            updated_index = startIndex + 1
            for ac in gameState.getLegalActions(startIndex):
                v = min(v, self.minValue(gameState.generateSuccessor(startIndex, ac), numberOfAgents, depth, updated_index))

            return v


    def maxValue(self, gameState, depth):
        if gameState.isWin() or depth == 0 or gameState.isLose():
            return self.evaluationFunction(gameState)

        v = -99999999

        for ac in gameState.getLegalActions(0):
            v = max(v, self.minValue(gameState.generateSuccessor(0, ac), gameState.getNumAgents(), depth, 1))

        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
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
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        v = self.maxValue(gameState, gameState.getNumAgents(), self.depth, 1, -99999999,99999999)

        # for ac in legalMoves:
        #     if v== self.evaluationFunction(gameState.generateSuccessor(0, ac)):
        #         return ac;
        return v

    def maxValue(self,gameState,numberOfAgents,depth,starIndex,alpha,beta):
        if gameState.isWin() or depth == 0 or gameState.isLose():
            return self.evaluationFunction(gameState)

        v = -99999999
        maxi = -99999999
        maxac = None
        for ac in gameState.getLegalActions(0):
            v = max(v, self.minValue(gameState.generateSuccessor(0, ac), gameState.getNumAgents(), depth, 1,alpha,beta))
            if v>maxi:
                maxi=v
                maxac=ac
            if v>beta and depth==self.depth:
                return ac
            if v>beta:
                return v
            alpha = max(alpha,v)

        if depth==self.depth:
            return maxac
        else:
            return v

    def minValue(self, gameState, numberOfAgents, depth, startIndex, alpha, beta):

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        v = 99999999

        if numberOfAgents == 2:
            depth -= 1
            for ac in gameState.getLegalActions(startIndex):
                v = min(v, self.maxValue(gameState.generateSuccessor(startIndex, ac), gameState.getNumAgents(),depth,1,alpha,beta))
                if v<alpha:
                    return v

                beta = min(beta,v)

            return v

        else:
            # call min
            numberOfAgents -= 1
            updated_index = startIndex + 1
            for ac in gameState.getLegalActions(startIndex):
                v = min(v, self.minValue(gameState.generateSuccessor(startIndex, ac), numberOfAgents, depth, updated_index,alpha,beta))
                if v<alpha:
                    return v
                beta = min(beta,v)


            return v



        # Choose one of the best actions
    #     scores = [self.minValue(gameState.generateSuccessor(0, action), gameState.getNumAgents(), self.depth, 1,-99999999,99999999) for
    #               action in legalMoves]
    #     bestScore = max(scores)
    #     bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    #     chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
    #
    #     "Add more of your code here if you want to"
    #
    #     return legalMoves[chosenIndex]
    #
    #     "*** YOUR CODE HERE ***"
    #     util.raiseNotDefined()
    #
    #
    # def minValue(self, gameState, numberOfAgents, depth, startIndex,alpha,beta):
    #     if gameState.isWin() or gameState.isLose():
    #         return self.evaluationFunction(gameState)
    #
    #     v = 99999999
    #
    #     if numberOfAgents == 2:
    #         depth -= 1
    #         for ac in gameState.getLegalActions(startIndex):
    #             v = min(v, self.maxValue(gameState.generateSuccessor(startIndex, ac), depth,alpha,beta))
    #             if v<alpha:
    #                 return v
    #             beta = min(beta,v)
    #
    #         return v
    #
    #     else:
    #         # call min
    #         numberOfAgents -= 1
    #         updated_index = startIndex + 1
    #         for ac in gameState.getLegalActions(startIndex):
    #             v = min(v, self.minValue(gameState.generateSuccessor(startIndex, ac), numberOfAgents, depth, updated_index,alpha,beta))
    #             if v<alpha:
    #                 return v
    #             beta = min(beta,v)
    #         return v
    #
    #
    # def maxValue(self, gameState, depth,alpha,beta):
    #     if gameState.isWin() or depth == 0 or gameState.isLose():
    #         return self.evaluationFunction(gameState)
    #
    #     v = -99999999
    #
    #     for ac in gameState.getLegalActions(0):
    #         v = max(v, self.minValue(gameState.generateSuccessor(0, ac), gameState.getNumAgents(), depth, 1,alpha,beta))
    #         if v>beta:
    #             return v
    #         alpha = max(alpha,v)
    #
    #     return v


class ExpectimaxAgent(MultiAgentSearchAgent):


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
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.minValue(gameState.generateSuccessor(0, action), gameState.getNumAgents(), self.depth, 1) for
                  action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


    def minValue(self, gameState, numberOfAgents, depth, startIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        v = 0

        if numberOfAgents == 2:
            depth -= 1
            prob= float(1.0/len(gameState.getLegalActions(startIndex)))
            for ac in gameState.getLegalActions(startIndex):
                v += prob*self.maxValue(gameState.generateSuccessor(startIndex, ac), depth)

            return v

        else:
            # call min
            numberOfAgents -= 1
            updated_index = startIndex + 1
            prob= float(1.0/len(gameState.getLegalActions(startIndex)))
            for ac in gameState.getLegalActions(startIndex):
                v += prob*self.minValue(gameState.generateSuccessor(startIndex, ac), numberOfAgents, depth, updated_index)

            return v


    def maxValue(self, gameState, depth):
        if gameState.isWin() or depth == 0 or gameState.isLose():
            return self.evaluationFunction(gameState)

        v = -99999999

        for ac in gameState.getLegalActions(0):
            v = max(v, self.minValue(gameState.generateSuccessor(0, ac), gameState.getNumAgents(), depth, 1))

        return v


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    successorGameState = currentGameState
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newFoodAsList = newFood.asList()
    newGhostPositions = currentGameState.getGhostPositions()
    capsules  = currentGameState.getCapsules()
	# distance to every food remanining
    sumOfDistanceToFood = []
	# distance to ghost
    sumOfDistanceToGhost = []
	
	# distance to every capsule i.e power pallets in the game
    sumOfDistanceToCapsule = []
    # print 'new pos:', newPos
    # print 'newFood:', newFoodAsList
    # print  'newScaredTimes', newScaredTimes
		
	# appending distance to every ghost in the scene	
    for newGh in newGhostPositions:
        sumOfDistanceToGhost.append(manhattanDistance(newPos, newGh))
	
	# appending distance to every capsule in the scene
    for cap in capsules:
        sumOfDistanceToCapsule.append(manhattanDistance(newPos, cap))
	
	# returning evaluation when there are food pallets remaining
    if len(newFoodAsList) > 0:
	
        # appending distance to every pallet in the scene
        for newFd in newFoodAsList:
            sumOfDistanceToFood.append(manhattanDistance(newPos, newFd))
        
		# if minimum distance to ghost is less than equal to 1 , then run away from ghost
        if min(sumOfDistanceToGhost)<=1:
            return -99999;
        
		# if ghost is scared then eat the ghost, therby putting high coefficient to distance nearest ghost
        if newScaredTimes[0] > 0:
            return currentGameState.getScore() + 10.7 / min(sumOfDistanceToFood) +  (80 * (1 / (min(sumOfDistanceToGhost) + .2)))
		
		# else eval the state using minimum distance to food and minimum distance to ghost
        else:
            return currentGameState.getScore() + 10.7 / min(sumOfDistanceToFood) - (27.7 * (1 / (min(sumOfDistanceToGhost) + .2)))
			
			# magnitude of coefficients is decided by trial and error 
    else:
		# when there are no pallets then return max value
        return 99999


# Abbreviation
better = betterEvaluationFunction


def manhattanDistance(xy1, xy2, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"

    return (abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1]))

# def mazeDistance(point1, point2, gameState):
#     """
#     Returns the maze distance between any two points, using the search functions
#     you have already built. The gameState can be any game state -- Pacman's
#     position in that state is ignored.
#
#     Example usage: mazeDistance( (2,4), (5,6), gameState)
#
#     This might be a useful helper function for your ApproximateSearchAgent.
#     """
#     x1, y1 = point1
#     x2, y2 = point2
#     walls = gameState.getWalls()
#     assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
#     assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
#     prob = search.SearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
#     return len(search.bfs(prob))
