# -*- coding: utf-8 -*-
# File: Player.py
# Author(s) names AND netid's: Josiah Evans, jge842, Shang Jiang, sjx371, Yang Wu, ywx108
# Date: 4/22/2016
# Group work statement: All group members were present and contributing during all work on this project
#      
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.

from __future__ import division
from random import *
from decimal import *
from copy import *
from MancalaBoard import *
from math import log, sqrt
import time

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=11):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 11)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    def fastCopy(self, board):
        """Quickly creates a new instance of the given board"""
        fcopy = MancalaBoard()
        fcopy.NCUPS = board.NCUPS
        fcopy.P1Cups = board.P1Cups[:]
        fcopy.P2Cups = board.P2Cups[:]
        fcopy.scoreCups = board.scoreCups[:]
        return fcopy

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        alpha = - INFINITY
        beta = INFINITY
        opponent = jge842(self.opp, self.type, self.ply)
        if ply == 0:
            return (self.score(board), board.legalMoves(self)[0])
        for m in board.legalMoves(self):
            #for each legal move
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            s = opponent.min_value(nb, ply-1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move 
        return (score, move)
    
    def max_value(self, board, ply, turn, a,b):
	"""Return the max value from this board position with alpha beta pruning"""
        alpha=a
        beta =b
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = jge842(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.min_value(nextBoard, ply-1, turn, alpha, beta)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
            if score >= beta:
                return score
            alpha = max(alpha, score)
        return score
        
    def max_value_bonus(self, board, ply, turn, a, b):
	"""Return the max value from this board position including bonus moves"""
        alpha = a
        beta = b
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        # make a new player to play the other side
        opponent = jge842(self.opp, self.type, self.ply)
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # Copy the board so that we don't ruin it
            nextBoard = self.fastCopy(board)
            #Check if max goes again
            if nextBoard.makeMove(self, m):
                s = self.max_value_bonus(nextBoard, ply-1, turn, alpha, beta)
            else:
                s = opponent.min_value_bonus(nextBoard, ply-1, turn, alpha, beta)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
            if score >= beta:
                return score
            alpha = max(alpha, score)
        return score
    
    def min_value(self, board, ply, turn,a,b):
	"""Return the minimum value from this board position using alpha beta pruning"""
        alpha=a
        beta=b
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = jge842(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.max_value(nextBoard, ply-1, turn, alpha, beta)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
            if score <= alpha:
                return score
            beta=min(beta, score)
        return score
        
    def min_value_bonus(self, board, ply, turn, a, b):
	"""Return the minimum value from this baord position accounting for bonus moves"""
        alpha=a
        beta=b
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        # make a new player to play the other side
        opponent = jge842(self.opp, self.type, self.ply)
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # Copy the board so that we don't ruin it
            nextBoard = self.fastCopy(board)
            if nextBoard.makeMove(self, m):
                s = self.min_value_bonus(nextBoard, ply-1, turn, alpha, beta)
            else:
                s = opponent.max_value_bonus(nextBoard, ply-1, turn, alpha, beta)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
            if score <= alpha:
                return score
            beta = min(beta, score)
        return score
                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            val, move = self.monteCarloSearchMove(board)
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1
            
    def alphaBetaMoveMonte(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        alpha = -INFINITY
        beta = INFINITY
        opponent = jge842(self.opp, self.type, self.ply)
        legalMoves = board.legalMoves(self)
            
        for m in legalMoves:
            #for each legal move
            nb = self.fastCopy(board)
            #make a new board
            #try the move, then check if we can go again.
            #initialize s
            if nb.makeMove(self, m):
                s = self.max_value_bonus(nb, ply - 1, turn, alpha, beta)
            else:
                s = opponent.min_value_bonus(nb, ply - 1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move 
        return move, s
        
    def abPruneBonus(self, board, ply):
        """ Choose a move with alpha beta pruning accounting for bonus moves.  Returns (score, move) """
        t0 = time.clock()
        move = -1
        score = -INFINITY
        turn = self
        alpha = -INFINITY
        beta = INFINITY
        opponent = jge842(self.opp, self.type, self.ply)
        legalMoves = board.legalMoves(self)
        if ply == 0:
            return (self.score(board), legalMoves[0])
            
        print len(legalMoves), " legal moves"
        for m in legalMoves:
            #for each legal move
            nb = self.fastCopy(board)
            #make a new board
            #try the move, then check if we can go again.
            #initialize s
            if nb.makeMove(self, m):
                s = self.max_value_bonus(nb, ply - 1, turn, alpha, beta)
            else:
                s = opponent.min_value_bonus(nb, ply - 1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move 
        t1 = time.clock()
        print t1 - t0, "seconds to move"
        return (score, move)

    def monteCarloSearchMove(self, board):
        """Performs a monte carlo tree search of the game space and selects the best move"""
        t0 = time.clock()
        #Create a monte carlo object
        self.mc = MonteCarlo(board, self)
        #Check if it is the first move
        opening = MancalaBoard()
        if repr(board) == repr(opening):
            return (1.0, 3)
        #Check if it is the second move
        opening.makeMove(self, 3)
        if repr(board) == repr(opening):
            return (1.0, 6)
        #Perform a hybrid Monte-carlo alpha-beta search of the game space
        move, pw = self.mc.getPlay()
        t1 = time.clock()
        print t1 - t0, "seconds to move"
        return (pw, move)

class MonteCarlo(object):
    """Monte Carlo object adapted from https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/"""
    def __init__(self, board, player, calculationTime=9.9):
        self.board = board
        self.calculationTime = calculationTime
        self.maxMoves = 100
        self.player = player
        self.wins = {}
        self.plays = {}
        self.c = 1.8
        self.interval1 = 36
        self.interval2 = 24
        self.interval3 = 12
        self.c1 = 12
        self.c2 = 6
        self.c3 = 3
        self.c4 = 1.5

    def fastCopy(self, board):
        """Quickly creates a new instance of the given board"""
        fcopy = MancalaBoard()
        fcopy.NCUPS = board.NCUPS
        fcopy.P1Cups = board.P1Cups[:]
        fcopy.P2Cups = board.P2Cups[:]
        fcopy.scoreCups = board.scoreCups[:]
        return fcopy

    def getPlay(self):
        """Do a monte carlo search of the game space and return the move with the highest win percentage"""
        print ""
        print "Player ", self.player.num
        print "searching game space"
        self.max_depth = 0
        state = self.fastCopy(self.board)
        player = self.player
        legal = state.legalMoves(player)
        if not legal:
            #no possible moves
            return 
        if len(legal) == 1:
            #Only one move to consider, so just do it
            return legal[0], .5

        games = 0
        #Pre-initialize variables for simulation
        plays, wins = self.plays, self.wins
        opponent = jge842(player.opp, player.type)
        maxMoves = self.maxMoves
        fastCopy = self.fastCopy
        t0 = time.clock()
        runSimulation = self.runSimulation
        calcTime = self.calculationTime
        playerNum = player.num

        while time.clock() - t0 < calcTime:
            #Run simulations of the game until we run out of time
            runSimulation(plays, wins, state, player, opponent, maxMoves, fastCopy, playerNum)
            games += 1

        print games, " games played"
        moves_states = []
        #Create states to lookup
        for p in legal:
            nb = self.fastCopy(state)
            nb.makeMove(player, p)
            moves_states.append((p, nb))

        moveScores = []
        moveWins = []
        movePlays = []

        #Lookup the win percentages for each move
        for p, S in moves_states:
            totalwins = self.wins[(repr(player), repr(S))]
            moveWins.append(totalwins)
            totalplays = self.plays[(repr(player), repr(S))]
            movePlays.append(totalplays)
            moveScores.append(totalwins / totalplays)
            
        #Choose the move with the highest win percentage
        percent_wins = moveScores[moveScores.index(max(moveScores))]
        move = legal[moveScores.index(max(moveScores))]

        print "Play Distribution"
        print movePlays
        print "Win Distribution"
        print moveWins
        return move, percent_wins

    def runSimulation(self, plays, wins, board, player, opponent, maxMoves, fastCopy, playerNum):
        #Initialize variables for simulation
        visited_states = set()
        expand = True
        goAgain = {}
        currPlayer = player
        playerList = [player, opponent]
        playerIndex = 0
        state = fastCopy(board)
        numStones = 48 - (state.scoreCups[playerList[0].num - 1] + state.scoreCups[playerList[1].num - 1])
        
        #Adjust Monte Carlo search parameters
        if numStones > self.interval1:
            self.c = self.c1
        elif numStones > self.interval2:
            self.c = self.c2
        elif numStones > self.interval3:
            self.c = self.c3
        else:
            self.c = self.c4

        #Go down the search space until we hit the maximum search depth
        for t in xrange(1, maxMoves + 1):
            legal = state.legalMoves(currPlayer)
            moves_states = []
            mStates = {}
            #Store possible moves at this state
            for p in legal:
                nb = fastCopy(state)
                goAgain[p] = nb.makeMove(currPlayer, p)
                moves_states.append((p, nb))
                mStates[p] = nb

            #If we have statistics for each possible state, then choose one based on c value weighted toward more promising branches
            if all(plays.get((repr(currPlayer), repr(S))) for p, S in moves_states) and currPlayer.num == playerNum:
                log_total = log(sum(plays[(repr(currPlayer), repr(S))] for p, S in moves_states))
                value, move, state = max(
                    ((wins[(repr(currPlayer), repr(S))] / plays[(repr(currPlayer), repr(S))]) + self.c * sqrt(log_total / plays[(repr(currPlayer), repr(S))]), p, S)
                    for p, S in moves_states)
            else:
                #If it is our opponent's turn, guess what he will do with alphaBetaBonus of varying ply depending on the number of stones left
                if currPlayer.num != playerNum:
                    numStones = 48 - (state.scoreCups[playerList[0].num - 1] + state.scoreCups[playerList[1].num - 1])
                    chance = random()
                    #Give opponent a 10% chance to make a move other than our guess
                    if chance < .9:
                        if numStones < 12:
                            move, q = currPlayer.alphaBetaMoveMonte(state, 4)
                            state = mStates[move]
                        elif numStones < 24:
                            move, q = currPlayer.alphaBetaMoveMonte(state, 3)
                            state = mStates[move]
                        else:
                            move, q = currPlayer.alphaBetaMoveMonte(state, 2)
                            state = mStates[move]
                    else:
                        move, state = choice(moves_states)
                else:
                    #If it is our turn, choose randomly 80% of the time, 20% of the time use alpha-beta with ply 5
                    chance = random()
                    if chance < .2:
                        move, q = currPlayer.alphaBetaMoveMonte(state, 5)
                        state = mStates[move]
                    else:
                        move, state = choice(moves_states)
                
            #If this is an expansion node, add it to the dictionary of plays and wins
            if expand and (repr(currPlayer), repr(state)) not in plays:
                expand = False
                self.plays[(repr(currPlayer), repr(state))] = 0
                self.wins[(repr(currPlayer), repr(state))] = 0
                expandedState = (repr(currPlayer), repr(state))
                if t > self.max_depth:
                    self.max_depth = t

            if (repr(currPlayer), repr(state)) in self.plays:
                visited_states.add((repr(currPlayer), repr(state)))
            
            #If we have already lost, stop searching the rest of the moves in this branch
            cutoff = False
            if state.scoreCups[currPlayer.num - 1] >= 25:
                cutoff = True
            #If we are losing badly, consider this branch a loss
            elif opponent.score(state) >= 30:
                cutoff = True
            over = state.gameOver()
            if over or cutoff:
                break

            #If we can't go again, change the player being simulated
            if not goAgain[move]:
                currPlayer = playerList[1 - playerIndex]
                playerIndex = 1 - playerIndex
                
            if t == maxMoves:
                print t

        #Update statistics for the expanded nodes in our tree that we visited.  
        for p, s in visited_states:
            plays[(p, s)] += 1
            if state.hasWon(playerNum) or state.scoreCups[player.num - 1] >= 25:
                wins[(p, s)] += 1




# Note, you should change the name of this player to be your netid
class jge842(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """
    def __init__(self, playerNum, playerType, ply = 11):
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply
        self.mc = MonteCarlo(MancalaBoard(), self)
        
    def fastCopy(self, board):
        """Quickly creates a new instance of the given board"""
        fcopy = MancalaBoard()
        fcopy.NCUPS = board.NCUPS
        fcopy.P1Cups = board.P1Cups[:]
        fcopy.P2Cups = board.P2Cups[:]
        fcopy.scoreCups = board.scoreCups[:]
        return fcopy

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        myscore = board.scoreCups[self.num - 1]
        theirscore = board.scoreCups[self.opp - 1]
            
        h1weight = 1.0
        h2weight = 1.0

        #First Heuristic = the score margin
        margin = myscore - theirscore
           
        #Second Heuristic = Stones on our side - stones on their side
        if self.num == 1:
            ourStones = sum(board.P1Cups)
            theirStones = sum(board.P2Cups)
        else:
            ourStones = sum(board.P2Cups)
            theirStones = sum(board.P1Cups)
            
        stoneMargin = ourStones - theirStones

        #Composite score
        return h1weight * margin - h2weight * stoneMargin
        

        
