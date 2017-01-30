# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    startState = [problem.getStartState(), 'Stop', 0]
   # print startState
    if problem.isGoalState(startState[0]):
        return startState[1]

    nodeStack = util.Stack();
    nodeStack.push(startState)
    exploredSet = set()
    while not nodeStack.isEmpty():
        tempNode = nodeStack.pop()
        if problem.isGoalState(tempNode[0]):
            return solution(tempNode)

        if tempNode[0] not in exploredSet:
            exploredSet.add(tempNode[0])
            for successor in problem.getSuccessors(tempNode[0]):
                child = [successor[0], " ".join((tempNode[1], successor[1])), 1]
                nodeStack.push(child)

    else:
        print 'No Solution Found'
        return ['Stop']
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    startState = [problem.getStartState(), 'Stop', 0]
   # print startState
    if problem.isGoalState(startState[0]):
        return startState[1]

    nodeQueue = util.Queue();
    nodeQueue.push(startState)
    exploredSet = set()
    while not nodeQueue.isEmpty():
        tempNode = nodeQueue.pop()
        if problem.isGoalState(tempNode[0]):
            return solution(tempNode)

        if tempNode[0] not in exploredSet:
            exploredSet.add(tempNode[0])
            for successor in problem.getSuccessors(tempNode[0]):
                child = [successor[0], " ".join((tempNode[1], successor[1])), 1]
                nodeQueue.push(child)

    else:
        print 'No Solution Found'
        return ['Stop']
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    startState = [problem.getStartState(), 'Stop', 0]
    #print startState
    if problem.isGoalState(startState[0]):
        return startState[1]

    nodePriorityQueue = util.PriorityQueue();
    nodePriorityQueue.push(startState,0)
    exploredSet = set()
    while not nodePriorityQueue.isEmpty():
        tempNode = nodePriorityQueue.pop()
        if problem.isGoalState(tempNode[0]):
            return solution(tempNode)

        if tempNode[0] not in exploredSet:
            exploredSet.add(tempNode[0])
            for successor in problem.getSuccessors(tempNode[0]):
                child = [successor[0], " ".join((tempNode[1], successor[1])), 1]
                tempList = child[1].split()
                #print "tempList",tempList
                tempCost = problem.getCostOfActions(tempList[1:])
                #print "tempcost" , tempCost
                nodePriorityQueue.push(child,tempCost)

    else:
        print 'No Solution Found'
        return ['Stop']
        util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = [problem.getStartState(), 'Stop', 0]
   # print startState
    if problem.isGoalState(startState[0]):
        return startState[1]

    nodePriorityQueue = util.PriorityQueue();
    nodePriorityQueue.push(startState, 0)
    exploredSet = set()
    while not nodePriorityQueue.isEmpty():
        tempNode = nodePriorityQueue.pop()
        if problem.isGoalState(tempNode[0]):
            return solution(tempNode)

        if tempNode[0] not in exploredSet:
            exploredSet.add(tempNode[0])
            for successor in problem.getSuccessors(tempNode[0]):
                child = [successor[0], " ".join((tempNode[1], successor[1])), 1]
                tempList = child[1].split()
                # print "tempList",tempList
                tempCost = problem.getCostOfActions(tempList[1:]) + heuristic(child[0],problem)
                # print "tempcost" , tempCost
                nodePriorityQueue.push(child, tempCost)

    else:
        print 'No Solution Found'
        return ['Stop']
        util.raiseNotDefined()
    util.raiseNotDefined()

def solution(x):
    tempList  = x[1].split()
    tempList.pop(0)
   # print len(tempList)
    directionList = tempList

    return directionList;

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
