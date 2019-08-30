# multiAgents.py
# --------------
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, math

from game import Agent
from operator import itemgetter

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

		score = 0

		#Values to adjust score
		#Ghost, food, remaining food
		scoreModifiers = [-50, 30, 10]



		##Ghost proximity
		currGhostPos = currentGameState.getGhostState(1).getPosition()
		succGhostPos = successorGameState.getGhostState(1).getPosition()

		if(newPos == currGhostPos or newPos == succGhostPos):
			score = score + scoreModifiers[0]
		else:
			score = score + scoreModifiers[0] / (util.manhattanDistance(newPos, succGhostPos))
		if util.manhattanDistance(newPos, succGhostPos) <= 1:
			score = score - 500


		#Food in next position
		if(currentGameState.hasFood(newPos[0], newPos[1])):
			score = score + scoreModifiers[1]


		#Remaining food on board
		for dot in successorGameState.getFood().asList():
			score = score - scoreModifiers[2] * (1 - 1/util.manhattanDistance(newPos, dot))


		return score

		# return successorGameState.getScore()



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

		return self.minimax(gameState, self.depth * 2, 0, True)[1]


		util.raiseNotDefined()


	def minimax(self, gameState, depth, agent, maxing):
		if(gameState.isWin() or gameState.isLose() or depth==0):
			return self.evaluationFunction(gameState), Directions.STOP


		legalActions = gameState.getLegalActions(agent)

		#maximizing
		if(maxing):
			actionScores = []
			for action in legalActions:
				actionScores.append((action, self.minimax(gameState.generateSuccessor(agent, action), depth-1, 1, False)[0]))

			bestAction, highestScore = max(actionScores,key=lambda item:item[1])
			return highestScore, bestAction

		#minimizing
		else:
			actionScores = []
			if agent == gameState.getNumAgents()-1: # switch from minimizing to maximizing
				for action in legalActions:
					actionScores.append((action, self.minimax(gameState.generateSuccessor(agent, action), depth-1, 0, True)[0]))
			else:
				for action in legalActions:
					actionScores.append((action, self.minimax(gameState.generateSuccessor(agent, action), depth, agent+1, False)[0]))

			bestAction, lowestScore = min(actionScores,key=lambda item:item[1])
			return lowestScore, bestAction




class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
		Returns the minimax action using self.depth and self.evaluationFunction
		"""
		
		return self.minimax(gameState, self.depth * 2, 0, True, -math.inf, math.inf)[1]

		util.raiseNotDefined()

	def minimax(self, gameState, depth, agent, maxing, alpha, beta):
		if(gameState.isWin() or gameState.isLose() or depth==0):
			return self.evaluationFunction(gameState), Directions.STOP


		#maximizing
		if(maxing):
			bestVal = -math.inf
			legalActions = gameState.getLegalActions(agent)
			actionScores = []
			for action in legalActions:
				value = self.minimax(gameState.generateSuccessor(agent, action), depth-1, 1, False, alpha, beta)[0]
				bestVal = max(bestVal, value)
				alpha = max(alpha, bestVal)
				
				actionScores.append((action, value))
				if beta < alpha:
					break
				# actionScores.append((action, value))

			bestAction, highestScore = max(actionScores,key=lambda item:item[1])
			return highestScore, bestAction

		#minimizing
		else:
			bestVal = math.inf
			legalActions = gameState.getLegalActions(agent)
			actionScores = []
			if agent == gameState.getNumAgents()-1: # switch from minimizing to maximizing
				for action in legalActions:
					value = self.minimax(gameState.generateSuccessor(agent, action), depth-1, 0, True, alpha, beta)[0]
					bestVal = min(bestVal, value)
					beta = min(beta, bestVal)

					actionScores.append((action, value))
					if beta < alpha:
						break
					# actionScores.append((action, value))
			else:
				for action in legalActions:
					value = self.minimax(gameState.generateSuccessor(agent, action), depth, agent+1, False, alpha, beta)[0]
					bestVal = min(bestVal, value)
					beta = min(beta, bestVal)

					actionScores.append((action, value))
					if beta < alpha:
						break


			bestAction, lowestScore = min(actionScores,key=lambda item:item[1])
			return lowestScore, bestAction

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
		return self.expectimax(gameState, self.depth*2, 0, True)[1]
		util.raiseNotDefined()

	def expectimax(self, gameState, depth, agent, maxing):
		if(gameState.isWin() or gameState.isLose() or depth==0):
			return self.evaluationFunction(gameState), Directions.STOP


		#maximizing
		if(maxing):
			legalActions = gameState.getLegalActions(agent)
			actionScores = []
			for action in legalActions:
				actionScores.append((action, self.expectimax(gameState.generateSuccessor(agent, action), depth-1, 1, False)[0]))

			bestAction, highestScore = max(actionScores,key=lambda item:item[1])
			return highestScore, bestAction

		#minimizing
		else:
			legalActions = gameState.getLegalActions(agent)
			actionScores = []
			if agent == gameState.getNumAgents()-1: # switch from minimizing to maximizing
				for action in legalActions:
					actionScores.append(self.expectimax(gameState.generateSuccessor(agent, action), depth-1, 0, True)[0])
			else:
				for action in legalActions:
					actionScores.append(self.expectimax(gameState.generateSuccessor(agent, action), depth, agent+1, False)[0])

			expectedScore = sum(actionScores) / len(actionScores)
			bestAction = random.choice(legalActions)
			return expectedScore, bestAction

def betterEvaluationFunction(currentGameState):
	"""
	Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	evaluation function (question 5).

	DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"


	currPos = currentGameState.getPacmanPosition()

	score = 0

	#Values to adjust score
	#Ghost, food, remaining food
	scoreModifiers = [-50, 30, 10, 20]


	#Incentivize eating food
	score = currentGameState.getScore() - 200.0 * currentGameState.getNumFood()

	#Run away if ghost is close
	currGhostPos = currentGameState.getGhostState(1).getPosition()
	if util.manhattanDistance(currPos, currGhostPos) <= 1:
		score = score - 500

	#Remaining food and capsules on board
	if(currentGameState.getFood().asList() != []):
		for dot in currentGameState.getFood().asList():
			score = score - scoreModifiers[2] * (1 - 1/util.manhattanDistance(currPos, dot))
		for powerPill in currentGameState.data.capsules:
			score = score - scoreModifiers[2] * (1 - 1/util.manhattanDistance(currPos, dot))


	return score
	util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
