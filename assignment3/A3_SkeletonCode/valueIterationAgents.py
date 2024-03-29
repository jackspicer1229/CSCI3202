# valueIterationAgents.py
# -----------------------

# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections, math

class ValueIterationAgent(ValueEstimationAgent):
		"""
				* Please read learningAgents.py before reading this.*

				A ValueIterationAgent takes a Markov decision process
				(see mdp.py) on initialization and runs value iteration
				for a given number of iterations using the supplied
				discount factor.
		"""
		def __init__(self, mdp, discount = 0.9, iterations = 100):
				"""
					Your value iteration agent should take an mdp on
					construction, run the indicated number of iterations
					and then act according to the resulting policy.

					Some useful mdp methods you will use:
							mdp.getStates()
							mdp.getPossibleActions(state)
							mdp.getTransitionStatesAndProbs(state, action)
							mdp.getReward(state, action, nextState)
							mdp.isTerminal(state)
				"""
				self.mdp = mdp
				self.discount = discount
				self.iterations = iterations
				self.values = util.Counter() # A Counter is a dict with default 0
				self.runValueIteration()

		def runValueIteration(self):
				# Write value iteration code here

				for i in range(0, self.iterations):
					states = self.mdp.getStates()
					curr_state_values = util.Counter()

					for state in states:
						max_val = -math.inf
						for action in self.mdp.getPossibleActions(state):
							q_val = self.computeQValueFromValues(state, action)
							if q_val > max_val:
								max_val = q_val

							curr_state_values[state] = max_val
					self.values = curr_state_values


		def getValue(self, state):
				"""
					Return the value of the state (computed in __init__).
				"""
				return self.values[state]


		def computeQValueFromValues(self, state, action):
				"""
					Compute the Q-value of action in state from the
					value function stored in self.values.
				"""
				
				q_val = 0
				for transition_state, transition_prob in self.mdp.getTransitionStatesAndProbs(state,action):
					reward = self.mdp.getReward(state, action, transition_state)
					trans_val = self.values[transition_state]
					q_val = q_val + (transition_prob * (reward + self.discount * trans_val))
				return q_val

				util.raiseNotDefined()

		def computeActionFromValues(self, state):
				"""
					The policy is the best action in the given state
					according to the values currently stored in self.values.

					You may break ties any way you see fit.  Note that if
					there are no legal actions, which is the case at the
					terminal state, you should return None.
				"""
				
				action_values = util.Counter()
				for action in self.mdp.getPossibleActions(state):
					action_values[action] = self.computeQValueFromValues(state, action)

				return action_values.argMax()

				util.raiseNotDefined()

		def getPolicy(self, state):
				return self.computeActionFromValues(state)

		def getAction(self, state):
				"Returns the policy at the state (no exploration)."
				return self.computeActionFromValues(state)

		def getQValue(self, state, action):
				return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
		"""
				* Please read learningAgents.py before reading this.*

				An AsynchronousValueIterationAgent takes a Markov decision process
				(see mdp.py) on initialization and runs cyclic value iteration
				for a given number of iterations using the supplied
				discount factor.
		"""
		def __init__(self, mdp, discount = 0.9, iterations = 1000):
				"""
					Your cyclic value iteration agent should take an mdp on
					construction, run the indicated number of iterations,
					and then act according to the resulting policy. Each iteration
					updates the value of only one state, which cycles through
					the states list. If the chosen state is terminal, nothing
					happens in that iteration.

					Some useful mdp methods you will use:
							mdp.getStates()
							mdp.getPossibleActions(state)
							mdp.getTransitionStatesAndProbs(state, action)
							mdp.getReward(state)
							mdp.isTerminal(state)
				"""
				ValueIterationAgent.__init__(self, mdp, discount, iterations)

		def runValueIteration(self):
				"*** YOUR CODE HERE ***"

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
		"""
				* Please read learningAgents.py before reading this.*

				A PrioritizedSweepingValueIterationAgent takes a Markov decision process
				(see mdp.py) on initialization and runs prioritized sweeping value iteration
				for a given number of iterations using the supplied parameters.
		"""
		def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
				"""
					Your prioritized sweeping value iteration agent should take an mdp on
					construction, run the indicated number of iterations,
					and then act according to the resulting policy.
				"""
				self.theta = theta
				ValueIterationAgent.__init__(self, mdp, discount, iterations)

		def runValueIteration(self):
				"*** YOUR CODE HERE ***"
