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

        "*** YOUR CODE HERE ***"
        #return successorGameState.getScore()
        food = currentGameState.getFood()
        currentPos = list(successorGameState.getPacmanPosition())
        distance = float("-Inf")

        foodList = food.asList()

        if action == 'Stop':
            return float("-Inf")

        for state in newGhostStates:
            if state.getPosition() == tuple(currentPos) and (state.scaredTimer == 0):
                return float("-Inf")

        for x in foodList:
            tempDistance = -1 * (manhattanDistance(currentPos, x))
            if (tempDistance > distance):
                distance = tempDistance

        return distance


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

    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

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
        #util.raiseNotDefined()
        def alphabeta(state):
            bestValue, bestAction = None, None
            # Start state
            # Store value
            value = []
            for action in state.getLegalActions(0):
                #value = max(value,minValue(state.generateSuccessor(0, action), 1, 1))
                succ  = minValue(state.generateSuccessor(0, action), 1, 1)
                value.append(succ)
                if bestValue is None:
                    bestValue = succ
                    bestAction = action
                else:
                    if succ > bestValue:
                        bestValue = succ
                        bestAction = action
            return bestAction

        def minValue(state, agentIdx, depth):
            # Check if we have taken all agent.
            if agentIdx == state.getNumAgents():
                return maxValue(state, 0, depth + 1)
            
            value = None
            # All action possible on current agentIdx
            for action in state.getLegalActions(agentIdx):
                # Only max value at Pacman state -> So all state will use minValue
                succ = minValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, depth)
                if value is None:
                    value = succ
                else:
                    value = min(value, succ)

            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)

        # Pacman state
        def maxValue(state, agentIdx, depth):
            if depth > self.depth:
                return self.evaluationFunction(state)
            value = None
            for action in state.getLegalActions(agentIdx):
                succ = minValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, depth)
                if value is None:
                    value = succ
                else:
                    value = max(value, succ)
                
            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)

        action = alphabeta(gameState)

        return action

        # def minimax_search(state, agentIndex, depth):
        #     # if in min layer and last ghost
        #     if agentIndex == state.getNumAgents():
        #         # if reached max depth, evaluate state
        #         if depth == self.depth:
        #             return self.evaluationFunction(state)
        #         # otherwise start new max layer with bigger depth
        #         else:
        #             return minimax_search(state, 0, depth + 1)
        #     # if not min layer and last ghost
        #     else:
        #         moves = state.getLegalActions(agentIndex)
        #         # if nothing can be done, evaluate the state
        #         if len(moves) == 0:
        #             return self.evaluationFunction(state)
        #         # get all the minimax values for the next layer with each node being a possible state after a move
        #         next = (minimax_search(state.generateSuccessor(agentIndex, m), agentIndex + 1, depth) for m in moves)

        #         # if max layer, return max of layer below
        #         if agentIndex == 0:
        #             return max(next)
        #         # if min layer, return min of layer below
        #         else:
        #             return min(next)
        # # select the action with the greatest minimax value
        # result = max(gameState.getLegalActions(0), key=lambda x: minimax_search(gameState.generateSuccessor(0, x), 1, 1))

        # return result        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        def alphabeta(state):
            bestValue, bestAction = None, None
            alpha = -9999999999
            beta = 9999999999

            value = []
            for action in state.getLegalActions(0):
                #value = max(value,minValue(state.generateSuccessor(0, action), 1, 1))
                succ  = minValue(state.generateSuccessor(0, action), 1, 1, alpha, beta)
                value.append(succ)
                if bestValue is None:
                    bestValue = succ
                    bestAction = action
                else:
                    if succ > bestValue:
                        bestValue = succ
                        bestAction = action
            return bestAction

        def minValue(state, agentIdx, depth, alpha, beta):
            # Check if we have taken all agent.
            if agentIdx == state.getNumAgents():
                return maxValue(state, 0, depth + 1, alpha, beta)
            
            value = None
            # All action possible on current agentIdx
            for action in state.getLegalActions(agentIdx):
                # Only max value at Pacman state -> So all state will use minValue
                succ = minValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, depth, alpha, beta)
                if value is None:
                    value = succ
                    if value <= alpha: return value
                    beta = min(beta, value)

                else:
                    value = min(value, succ)

            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)
        
        def maxValue(state, agentIdx, depth, alpha, beta):
            if depth > self.depth:
                return self.evaluationFunction(state)
            value = None
            for action in state.getLegalActions(agentIdx):
                succ = minValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, depth, alpha, beta)
                if value is None:
                    value = succ
                else:
                    value = max(value, succ)
                    if value > beta: return value
                    alpha = max(alpha, value)
            
            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)

        action = alphabeta(gameState)

        return action
        


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        def alphabeta(state):
            bestValue, bestAction = None, None
            # Start state
            # Store value
            value = []
            for action in state.getLegalActions(0):
                #value = max(value,minValue(state.generateSuccessor(0, action), 1, 1))
                succ  = expValue(state.generateSuccessor(0, action), 1, 1)
                value.append(succ)
                if bestValue is None:
                    bestValue = succ
                    bestAction = action
                else:
                    if succ > bestValue:
                        bestValue = succ
                        bestAction = action
            return bestAction

        def expValue(state, agentIdx, depth):
            # Check if we have taken all agent.
            if agentIdx == state.getNumAgents():
                return maxValue(state, 0, depth + 1)
            
            value = None
            # All action possible on current agentIdx
            p = 1 / (len(state.getLegalActions(agentIdx)) + 0.0001)
            for action in state.getLegalActions(agentIdx):
                # Only max value at Pacman state -> So all state will use minValue
                succ = expValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, depth)
                if value is None:
                    value = succ
                else:
                    value += p * succ

            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)

        # Pacman state
        def maxValue(state, agentIdx, depth):
            if depth > self.depth:
                return self.evaluationFunction(state)
            value = None
            for action in state.getLegalActions(agentIdx):
                succ = expValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, depth)
                if value is None:
                    value = succ
                else:
                    value = max(value, succ)
                
            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)

        action = alphabeta(gameState)

        return action

def oldEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newCapsules = currentGameState.getCapsules()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    closestGhost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
    if newCapsules:
        closestCapsule = min([manhattanDistance(newPos, caps) for caps in newCapsules])
    else:
        closestCapsule = 0

    if closestCapsule:
        closest_capsule = -3 / closestCapsule
    else:
        closest_capsule = 100

    if closestGhost:
        ghost_distance = -2 / closestGhost
    else:
        ghost_distance = -500

    foodList = newFood.asList()
    if foodList:
        closestFood = min([manhattanDistance(newPos, food) for food in foodList])
    else:
        closestFood = 0
        
    return closestFood + ghost_distance - len(foodList) + 1000 * closest_capsule + scoreEvaluationFunction(currentGameState)


def EuclidDistance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5

def betterEvaluationFunction(currentGameState):
    """
    Các đặc trưng trong game gồm những gì?
    - 1 - Điểm hiện tại: currentGameState.getScore()
    - 2 - Vị trí của Pacman: currentGameState.getPacmanPosition()
    - 3 - Vị trí của Ghost: currentGameState.getGhostStates()
    - 4 - Vị trí của Food: currentGameState.getFood()
    - 5 - Số lượng Food còn lại: len(4)
    - 6 - Vị trí của thức ăn đặc biệt: currentGameState.getCapsules()
    - 7 - Đặc điểm của ma khi dính effect: Ghost.scaredTimer > 0
    - 8 - Vị trí capsule currentGameState.getCapsules()

    Tránh bị mất điểm khi di chuyển những bước thừa: Add 1 
    Tránh Ghost chase (tránh xa ghost càng tốt (Không quá lớn là ok)? - Tránh bị kẹt 2 đầu là đủ, but how?) -> tránh terminate -> So sánh khoảng cách giữa ghost thường và ghost dính effect 
                -> Nếu ghost dính effect gần hơn thì tấn công ghost này. 3, 7
    Luôn tìm cách ăn hết thức ăn để kết thúc game và chiến thắng -> 5
    Hướng về thức ăn gần nhất có quan trọng không? 

    """
    newPos = currentGameState.getPacmanPosition() #2
    ghostState = currentGameState.getGhostStates() #3

    ghostDistance = 0
    effectGhostDistance = 0 #7

    for ghost in ghostState:
        if ghost.scaredTimer > 0:
            effectGhostDistance = min(effectGhostDistance, manhattanDistance(newPos, ghost.getPosition()))
        else:
            ghostDistance = min(manhattanDistance(newPos, ghost.getPosition()), ghostDistance)


    if effectGhostDistance != 0:
        if effectGhostDistance < ghostDistance:             
            print("dasdasddada", effectGhostDistance, ghostDistance)
            effectGhostDistance *= 2
        else: effectGhostDistance *= 3

    closestCapsule = 1000
    foodDistance = 0
    foodDistanceEuclid = 0


    foodList = currentGameState.getFood().asList() #4
    if foodList:
        foodDistance = max(0, min([manhattanDistance(newPos, food) for food in foodList]))
        foodDistanceEuclid = max(0, min([EuclidDistance(newPos, food) for food in foodList]))

    newCapsules = currentGameState.getCapsules() #8


    if newCapsules:
        closestCapsule = max(0, min([manhattanDistance(newPos, caps) for caps in newCapsules]))
        if closestCapsule > 5: closestCapsule = 1000
        closestCapsule *= 10
    else: closestCapsule = 0
    
    score = currentGameState.getScore() + (ghostDistance) + (effectGhostDistance) - 1.5 * (foodDistanceEuclid) - (len(foodList)) * 4 - (closestCapsule)

    return score


def finalEvaluationFunction(currentGameState):
    """
    Các đặc trưng trong game gồm những gì?
    - 1 - Điểm hiện tại: currentGameState.getScore()
    - 2 - Vị trí của Pacman: currentGameState.getPacmanPosition()
    - 3 - Vị trí của Ghost: currentGameState.getGhostStates()
    - 4 - Vị trí của Food: currentGameState.getFood()
    - 5 - Số lượng Food còn lại: len(4)
    - 6 - Vị trí của thức ăn đặc biệt: currentGameState.getCapsules()
    - 7 - Đặc điểm của ma khi dính effect: Ghost.scaredTimer > 0
    - 8 - Vị trí capsule currentGameState.getCapsules()

    Tránh bị mất điểm khi di chuyển những bước thừa: Add 1 
    Tránh Ghost chase (tránh xa ghost càng tốt (Không quá lớn là ok)? - Tránh bị kẹt 2 đầu là đủ, but how?) -> tránh terminate -> So sánh khoảng cách giữa ghost thường và ghost dính effect 
                -> Nếu ghost dính effect gần hơn thì tấn công ghost này. 3, 7
    Luôn tìm cách ăn hết thức ăn để kết thúc game và chiến thắng -> 5
    Hướng về thức ăn gần nhất có quan trọng không? 

    """
    newPos = currentGameState.getPacmanPosition() #2
    ghostState = currentGameState.getGhostStates() #3

    ghostDistance = 0
    effectGhostDistance = 200 #7

    for ghost in ghostState:
        if ghost.scaredTimer > 0:
            effectGhostDistance = min(effectGhostDistance, manhattanDistance(newPos, ghost.getPosition()))
        else:
            ghostDistance = min(manhattanDistance(newPos, ghost.getPosition()), ghostDistance)


    foodDistance = 0
    foodDistanceEuclid = 0


    foodList = currentGameState.getFood().asList() #4
    if foodList:
        foodDistance = max(0, min([manhattanDistance(newPos, food) for food in foodList]))
        foodDistanceEuclid = max(0, min([EuclidDistance(newPos, food) for food in foodList]))

    newCapsules = currentGameState.getCapsules() #8
    closestCapsuleGhost = 0
    

    closestCapsule = 100
    if newCapsules:
        closestCapsule = min([manhattanDistance(newPos, caps) for caps in newCapsules])
        if closestCapsule > 10: closestCapsule = 100
    else:
        closestCapsule = 0
    
    
    score = 2 * currentGameState.getScore() -  (len(foodList)) - foodDistanceEuclid - ghostDistance - 10 * (closestCapsule) - effectGhostDistance

    return score


# Abbreviation
better = betterEvaluationFunction