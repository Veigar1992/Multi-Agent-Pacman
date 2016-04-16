# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util, sys

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
#        print successorGameState
#        print 'here'
#        print newPos
#        print newFood
#        print newGhostStates
#        print newScaredTimes

        "*** YOUR CODE HERE ***"
        ghostposition=successorGameState.getGhostPositions()
        score=successorGameState.getScore()
#        print ghostposition
#        print score
#        exit(0)
        a = 0
        i=0
        z=0
        for x in newFood:
            i+=1
        for y in newFood[0]:
            z+=1
#        print"iiiiii",i
#        print"zzzz",z
#        exit(0)


        xpacman,ypacman=newPos
        if successorGameState.isLose():
            return -sys.maxint
        if successorGameState.isWin():
            return sys.maxint
        minfood=999
        minghost=999
        foodi = -1
        for foodx in range(i):

            for foody in range(z):
            	#print"foodx foody",foodx,foody

                dist = 0
                fg = False
                if newFood[foodx][foody] == True:
                    foodi+=1
                    fg = True
                    dist = abs(xpacman-foodx)+abs(ypacman-foody)+foodi
                if dist < minfood and fg:
                    minfood = dist

        index=0
        for x,y in ghostposition:
            index += 1
            if index == 2:
                exit(0)
            dis=abs(xpacman-x)+abs(ypacman-y)
            if dis<minghost:
                minghost=dis

        if minghost < 3:
            score+=minghost*4
        if minfood != 999:
            score-=minfood*0.01
        return score
        #successorGameState.getScore()

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
        """
        "*** YOUR CODE HERE ***"
        self.agentnum=gameState.getNumAgents()
        depth=self.depth
        agentindex=0
        (res, actionutility)=self.minimaxvalue(gameState,depth,agentindex)
        return res

    def minimaxvalue(self,gameState,depth,agentindex):
        actions=gameState.getLegalActions(agentindex)
        # end condition
        if depth==0 or len(actions)==0:
            utility=self.evaluationFunction(gameState)
            return ('',utility)
        # next agent index
        newagentindex = (agentindex + 1)%self.agentnum
        # next layer
        if newagentindex==0:depth-=1
        #Pacman
        if agentindex==0:
            utility=float("-inf")
            resaction = ''
            for action in actions:
                state=gameState.generateSuccessor(agentindex,action)
                stateutility=self.minimaxvalue(state,depth,newagentindex)
                if stateutility[1]>utility:
                    (resaction, utility)=(action, stateutility[1])
            return (resaction, utility)
        #ghost
        else:
            utility=float("inf")
            resaction = ''
            for action in actions:
                state=gameState.generateSuccessor(agentindex,action)
                stateutility=self.minimaxvalue(state,depth,newagentindex)
                if stateutility[1]<utility:
                    (resaction, utility)=(action, stateutility[1])
            return (resaction, utility)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self.agentnum=gameState.getNumAgents()
        depth=self.depth
        agentindex=0
        res, actionutility=self.minimaxvalue(gameState,depth,agentindex,float("-inf"),float("inf"))
        return res

    def minimaxvalue(self,gameState,depth,agentindex,alpha,beta):
        actions=gameState.getLegalActions(agentindex)
        # end condition
        if depth==0 or len(actions)==0:
            utility=self.evaluationFunction(gameState)
            return '',utility
        # next agent index
        newagentindex = (agentindex + 1)%self.agentnum
        # next layer
        if newagentindex==0:depth-=1
        #Pacman
        if agentindex==0:
            utility=float("-inf")
            resaction = ''
            for action in actions:
                state=gameState.generateSuccessor(agentindex,action)
                stateutility=self.minimaxvalue(state,depth,newagentindex,alpha,beta)
                if stateutility[1]>utility:
                    resaction, utility=action, stateutility[1]
                if utility > beta:
                    break
                alpha = max(alpha,utility)
            return resaction, utility
        #ghost
        else:
            utility=float("inf")
            resaction = ''
            for action in actions:
                state=gameState.generateSuccessor(agentindex,action)
                stateutility=self.minimaxvalue(state,depth,newagentindex,alpha,beta)
                if stateutility[1]<utility:
                    resaction, utility=action, stateutility[1]
                if utility < alpha:
                    break
                beta=min(beta, utility)
            return resaction, utility

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

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

