from MancalaBoard import MancalaBoard
from Player import Agent
from random import *
from copy import deepcopy


def adjust_player(player):
    chance = random()
    if chance < 1.0 / 7.0:
        player.mc.interval1 = player.mc.interval1 * (.5 + random())
    elif chance < 2.0 / 7.0:
        player.mc.interval2 = player.mc.interval2 * (.5 + random())
    elif chance < 3.0 / 7.0:
        player.mc.interval3 = player.mc.interval3 * (.5 + random())
    elif chance < 4.0 / 7.0:
        player.mc.c1 = player.mc.c1 * (.5 + random())
    elif chance < 5.0 / 7.0:
        player.mc.c2 = player.mc.c2 * (.5 + random())
    elif chance < 6.0 / 7.0:
        player.mc.c3 = player.mc.c3 * (.5 + random())
    else:
        player.mc.c4 = player.mc.c4 * (.5 + random())


def play_n_games(player1, player2, n):
    wins = 0
    for x in range(0, n):
        print("playing game ", x, " of ", n)
        board = MancalaBoard()
        board.hostGame(player1, player2)
        if board.hasWon(player1.num):
            wins += 1
    return wins / float(n)


def play_n_rounds(num_players, num_rounds, num_games):
    players = [Agent(1, 4, 9), Agent(1, 4, 9)]
    players[0].mc.calculation_time = 5
    players[1].mc.calculation_time = 5
    win_ratios = {}
    abprune = Agent(2, 3, 10)
    generation = 0
    while generation < num_rounds:
        print("round ", generation + 1, "of ", num_rounds)
        while len(players) < num_players:
            chance = random()
            if chance < .5:
                new_player = deepcopy(players[0])
            else:
                new_player = deepcopy(players[1])
            adjust_player(new_player)
            players.append(new_player)
            win_ratios[new_player] = 0

        for p in players:
            win_ratios[p] = play_n_games(p, abprune, num_games)

        toptwo = []
        for p in players:
            if len(toptwo) < 2:
                toptwo.append(p)
            else:
                for t in toptwo:
                    if win_ratios[p] > win_ratios[t]:
                        toptwo.append(p)
                        toptwo.remove(t)
                        break
        players = toptwo
        for p in players:
            mc = p.mc
            print(mc.interval1, mc.interval2, mc.interval3, mc.c1,
                  mc.c2, mc.c3, mc.c4, win_ratios[p])

        generation += 1
    first = players[0].mc
    second = players[1].mc
    return (first.interval1, first.interval2, first.interval3, first.c1,
            first.c2, first.c3, first.c4, win_ratios[players[0]], second.interval1, second.interval2,
            second.interval3, second.c1, second.c2, second.c3, second.c4, win_ratios[players[1]])


print()
play_n_rounds(4, 2, 2)
# First Generation
