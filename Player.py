# -*- coding: utf-8 -*-
# File: Player.py
# Author(s) names: Josiah Evans, Shang Jiang, Yang Wu
# Date: 4/22/2016
# Group work statement: All group members were present and contributing during all work on this project
#      
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.

from __future__ import division
from MancalaBoard import MancalaBoard
from math import log, sqrt
from copy import deepcopy
from random import choice, random
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

    def __init__(self, player_num, player_type, ply=11):
        """Initialize a Player with a player_num (1 or 2), player_type (one of
        the constants such as HUMAN), and a ply (default is 11)."""
        self.num = player_num
        self.opp = 2 - player_num + 1
        self.type = player_type
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)

    def minimax_move(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            # for each legal move
            if ply == 0:
                # if we're at ply 0, we need to call our eval function & return
                return self.score(board), m
            if board.gameOver():
                return -1, -1  # Can't make a move, the game is over
            nb = deepcopy(board)
            # make a new board
            nb.makeMove(self, m)
            # try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minmax_min_value(nb, ply - 1, turn)
            # and see what the opponent would do next
            if s > score:
                # if the result is better than our best score so far, save that move,score
                move = m
                score = s
        # return the best score and move so far
        return score, move

    def minmax_max_value(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuration. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                # print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            next_board = deepcopy(board)
            next_board.makeMove(self, m)
            s = opponent.minmax_min_value(next_board, ply - 1, turn)
            # print "s in minmax_max_value is: " + str(s)
            if s > score:
                score = s
        return score

    def minmax_min_value(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuration. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                # print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            next_board = deepcopy(board)
            next_board.makeMove(self, m)
            s = opponent.minmax_max_value(next_board, ply - 1, turn)
            # print "s in minmax_min_value is: " + str(s)
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

    def fast_copy(self, board):
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
    def alpha_beta_move(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        alpha = - INFINITY
        beta = INFINITY
        opponent = Agent(self.opp, self.type, self.ply)
        if ply == 0:
            return self.score(board), board.legalMoves(self)[0]
        for m in board.legalMoves(self):
            # for each legal move
            nb = deepcopy(board)
            # make a new board
            nb.makeMove(self, m)
            # try the move
            s = opponent.ab_min_value(nb, ply - 1, turn, alpha, beta)
            # and see what the opponent would do next
            if s > score:
                # if the result is better than our best score so far, save that move,score
                move = m
                score = s
        # return the best score and move
        return score, move

    def max_value(self, board, ply, turn, a, b):
        """Return the max value from this board position with alpha beta pruning"""
        alpha = a
        beta = b
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                # print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Agent(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            next_board = deepcopy(board)
            next_board.makeMove(self, m)
            s = opponent.ab_min_value(next_board, ply - 1, turn, alpha, beta)
            # print "s in minmax_max_value is: " + str(s)
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
        opponent = Agent(self.opp, self.type, self.ply)
        for m in board.legalMoves(self):
            if ply == 0:
                # print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # Copy the board so that we don't ruin it
            next_board = self.fast_copy(board)
            # Check if max goes again
            if next_board.makeMove(self, m):
                s = self.max_value_bonus(next_board, ply - 1, turn, alpha, beta)
            else:
                s = opponent.min_value_bonus(next_board, ply - 1, turn, alpha, beta)
            # print "s in minmax_max_value is: " + str(s)
            if s > score:
                score = s
            if score >= beta:
                return score
            alpha = max(alpha, score)
        return score

    def ab_min_value(self, board, ply, turn, a, b):
        """Return the minimum value from this board position using alpha beta pruning"""
        alpha = a
        beta = b
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                # print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Agent(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            next_board = deepcopy(board)
            next_board.makeMove(self, m)
            s = opponent.max_value(next_board, ply - 1, turn, alpha, beta)
            # print "s in minmax_min_value is: " + str(s)
            if s < score:
                score = s
            if score <= alpha:
                return score
            beta = min(beta, score)
        return score

    def min_value_bonus(self, board, ply, turn, a, b):
        """Return the minimum value from this baord position accounting for bonus moves"""
        alpha = a
        beta = b
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        # make a new player to play the other side
        opponent = Agent(self.opp, self.type, self.ply)
        for m in board.legalMoves(self):
            if ply == 0:
                # print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # Copy the board so that we don't ruin it
            next_board = self.fast_copy(board)
            if next_board.makeMove(self, m):
                s = self.min_value_bonus(next_board, ply - 1, turn, alpha, beta)
            else:
                s = opponent.max_value_bonus(next_board, ply - 1, turn, alpha, beta)
            # print "s in minmax_min_value is: " + str(s)
            if s < score:
                score = s
            if score <= alpha:
                return score
            beta = min(beta, score)
        return score

    def choose_move(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print(move, "is not valid")
                move = input("Please enter your move")
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print("chose move", move)
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimax_move(board, self.ply)
            print("chose move", move, " with value", val)
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alpha_beta_move(board, self.ply)
            print("chose move", move, " with value", val)
            return move
        elif self.type == self.CUSTOM:
            val, move = self.monte_carlo_search_move(board)
            print("chose move", move, " with value", val)
            return move
        else:
            print("Unknown player type")
            return -1

    def alpha_beta_move_monte(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        alpha = -INFINITY
        beta = INFINITY
        opponent = Agent(self.opp, self.type, self.ply)
        legal_moves = board.legalMoves(self)

        for m in legal_moves:
            # for each legal move
            nb = self.fast_copy(board)
            # make a new board
            # try the move, then check if we can go again.
            # initialize s
            if nb.makeMove(self, m):
                s = self.max_value_bonus(nb, ply - 1, turn, alpha, beta)
            else:
                s = opponent.min_value_bonus(nb, ply - 1, turn, alpha, beta)
            # and see what the opponent would do next
            if s > score:
                # if the result is better than our best score so far, save that move,score
                move = m
                score = s
        # return the best score and move
        return move, s

    def ab_prune_bonus(self, board, ply):
        """ Choose a move with alpha beta pruning accounting for bonus moves.  Returns (score, move) """
        t0 = time.clock()
        move = -1
        score = -INFINITY
        turn = self
        alpha = -INFINITY
        beta = INFINITY
        opponent = Agent(self.opp, self.type, self.ply)
        legal_moves = board.legalMoves(self)
        if ply == 0:
            return self.score(board), legal_moves[0]

        print(len(legal_moves), " legal moves")
        for m in legal_moves:
            # for each legal move
            nb = self.fast_copy(board)
            # make a new board
            # try the move, then check if we can go again.
            # initialize s
            if nb.makeMove(self, m):
                s = self.max_value_bonus(nb, ply - 1, turn, alpha, beta)
            else:
                s = opponent.min_value_bonus(nb, ply - 1, turn, alpha, beta)
            # and see what the opponent would do next
            if s > score:
                # if the result is better than our best score so far, save that move,score
                move = m
                score = s
        # return the best score and move
        t1 = time.clock()
        print(t1 - t0, "seconds to move")
        return score, move

    def monte_carlo_search_move(self, board):
        """Performs a monte carlo tree search of the game space and selects the best move"""
        t0 = time.clock()
        # Create a monte carlo object
        self.mc = MonteCarlo(board, self)
        # Check if it is the first move
        opening = MancalaBoard()
        if repr(board) == repr(opening):
            return 1.0, 3
        # Check if it is the second move
        opening.makeMove(self, 3)
        if repr(board) == repr(opening):
            return 1.0, 6
        # Perform a hybrid Monte-carlo alpha-beta search of the game space
        move, pw = self.mc.get_play()
        t1 = time.clock()
        print(t1 - t0, "seconds to move")
        return pw, move


class MonteCarlo(object):
    """Monte Carlo object adapted from https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/"""

    def __init__(self, board, player, calculation_time=9.9):
        self.board = board
        self.calculation_time = calculation_time
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

    @staticmethod
    def fast_copy(board):
        """Quickly creates a new instance of the given board"""
        fcopy = MancalaBoard()
        fcopy.NCUPS = board.NCUPS
        fcopy.P1Cups = board.P1Cups[:]
        fcopy.P2Cups = board.P2Cups[:]
        fcopy.scoreCups = board.scoreCups[:]
        return fcopy

    def get_play(self):
        """Do a monte carlo search of the game space and return the move with the highest win percentage"""
        print("")
        print("Player ", self.player.num)
        print("searching game space")
        self.max_depth = 0
        state = self.fast_copy(self.board)
        player = self.player
        legal = state.legalMoves(player)
        if not legal:
            # no possible moves
            return
        if len(legal) == 1:
            # Only one move to consider, so just do it
            return legal[0], .5

        games = 0
        # Pre-initialize variables for simulation
        plays, wins = self.plays, self.wins
        opponent = Agent(player.opp, player.type)
        max_moves = self.maxMoves
        fast_copy = self.fast_copy
        t0 = time.clock()
        run_simulation = self.run_simulation
        calc_time = self.calculation_time
        player_num = player.num

        while time.clock() - t0 < calc_time:
            # Run simulations of the game until we run out of time
            run_simulation(plays, wins, state, player, opponent, max_moves, fast_copy, player_num)
            games += 1

        print(games, " games played")
        moves_states = []
        # Create states to lookup
        for p in legal:
            nb = self.fast_copy(state)
            nb.makeMove(player, p)
            moves_states.append((p, nb))

        move_scores = []
        move_wins = []
        move_plays = []

        # Lookup the win percentages for each move
        for p, S in moves_states:
            totalwins = self.wins[(repr(player), repr(S))]
            move_wins.append(totalwins)
            totalplays = self.plays[(repr(player), repr(S))]
            move_plays.append(totalplays)
            move_scores.append(totalwins / totalplays)

        # Choose the move with the highest win percentage
        percent_wins = move_scores[move_scores.index(max(move_scores))]
        move = legal[move_scores.index(max(move_scores))]

        print("Play Distribution")
        print(move_plays)
        print("Win Distribution")
        print(move_wins)
        return move, percent_wins

    def run_simulation(self, plays, wins, board, player, opponent, maxMoves, fastCopy, playerNum):
        # Initialize variables for simulation
        visited_states = set()
        expand = True
        go_again = {}
        curr_player = player
        player_list = [player, opponent]
        player_index = 0
        state = fastCopy(board)
        num_stones = 48 - (state.scoreCups[player_list[0].num - 1] + state.scoreCups[player_list[1].num - 1])

        # Adjust Monte Carlo search parameters
        if num_stones > self.interval1:
            self.c = self.c1
        elif num_stones > self.interval2:
            self.c = self.c2
        elif num_stones > self.interval3:
            self.c = self.c3
        else:
            self.c = self.c4

        # Go down the search space until we hit the maximum search depth
        for t in range(1, maxMoves + 1):
            legal = state.legalMoves(curr_player)
            moves_states = []
            mStates = {}
            # Store possible moves at this state
            for p in legal:
                nb = fastCopy(state)
                go_again[p] = nb.makeMove(curr_player, p)
                moves_states.append((p, nb))
                mStates[p] = nb

            # If we have statistics for each possible state, then choose one based on c value weighted toward more
            # promising branches
            if all(plays.get((repr(curr_player), repr(S))) for p, S in moves_states) and curr_player.num == playerNum:
                log_total = log(sum(plays[(repr(curr_player), repr(S))] for p, S in moves_states))
                value, move, state = max(
                    ((wins[(repr(curr_player), repr(S))] / plays[(repr(curr_player), repr(S))]) + self.c * sqrt(
                        log_total / plays[(repr(curr_player), repr(S))]), p, S)
                    for p, S in moves_states)
            else:
                # If it is our opponent's turn, guess what he will do with alphaBetaBonus of varying ply depending on
                # the number of stones left
                if curr_player.num != playerNum:
                    num_stones = 48 - (state.scoreCups[player_list[0].num - 1] + state.scoreCups[player_list[1].num - 1])
                    chance = random()
                    # Give opponent a 10% chance to make a move other than our guess
                    if chance < .9:
                        if num_stones < 12:
                            move, q = curr_player.alpha_beta_move_monte(state, 4)
                            state = mStates[move]
                        elif num_stones < 24:
                            move, q = curr_player.alpha_beta_move_monte(state, 3)
                            state = mStates[move]
                        else:
                            move, q = curr_player.alpha_beta_move_monte(state, 2)
                            state = mStates[move]
                    else:
                        move, state = choice(moves_states)
                else:
                    # If it is our turn, choose randomly 80% of the time, 20% of the time use alpha-beta with ply 5
                    chance = random()
                    if chance < .2:
                        move, q = curr_player.alpha_beta_move_monte(state, 5)
                        state = mStates[move]
                    else:
                        move, state = choice(moves_states)

            # If this is an expansion node, add it to the dictionary of plays and wins
            if expand and (repr(curr_player), repr(state)) not in plays:
                expand = False
                self.plays[(repr(curr_player), repr(state))] = 0
                self.wins[(repr(curr_player), repr(state))] = 0
                expandedState = (repr(curr_player), repr(state))
                if t > self.max_depth:
                    self.max_depth = t

            if (repr(curr_player), repr(state)) in self.plays:
                visited_states.add((repr(curr_player), repr(state)))

            # If we have already lost, stop searching the rest of the moves in this branch
            cutoff = False
            if state.scoreCups[curr_player.num - 1] >= 25:
                cutoff = True
            # If we are losing badly, consider this branch a loss
            elif opponent.score(state) >= 30:
                cutoff = True
            over = state.gameOver()
            if over or cutoff:
                break

            # If we can't go again, change the player being simulated
            if not go_again[move]:
                curr_player = player_list[1 - player_index]
                player_index = 1 - player_index

            if t == maxMoves:
                print(t)

        # Update statistics for the expanded nodes in our tree that we visited.
        for p, s in visited_states:
            plays[(p, s)] += 1
            if state.hasWon(playerNum) or state.scoreCups[player.num - 1] >= 25:
                wins[(p, s)] += 1


# Note, you should change the name of this player to be your netid
class Agent(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def __init__(self, player_num, player_type, ply=11):
        super().__init__(player_num, player_type, ply)
        self.num = player_num
        self.opp = 2 - player_num + 1
        self.type = player_type
        self.ply = ply
        self.mc = MonteCarlo(MancalaBoard(), self)

    def fast_copy(self, board):
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

        # First Heuristic = the score margin
        margin = myscore - theirscore

        # Second Heuristic = Stones on our side - stones on their side
        if self.num == 1:
            our_stones = sum(board.P1Cups)
            their_stones = sum(board.P2Cups)
        else:
            our_stones = sum(board.P2Cups)
            their_stones = sum(board.P1Cups)

        stone_margin = our_stones - their_stones

        # Composite score
        return h1weight * margin - h2weight * stone_margin
