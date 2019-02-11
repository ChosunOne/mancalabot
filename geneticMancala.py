from Player import *
from MancalaBoard import *
from MancalaGUI import *
from random import *

def adjustPlayer(player):
    chance = random()
    if chance < 1.0/7.0:
        player.mc.interval1 = player.mc.interval1 * (.5 + random())
    elif chance < 2.0/7.0:
        player.mc.interval2 = player.mc.interval2 * (.5 + random())
    elif chance < 3.0/7.0:
        player.mc.interval3 = player.mc.interval3 * (.5 + random())
    elif chance < 4.0/7.0:
        player.mc.c1 = player.mc.c1 * (.5 + random())
    elif chance < 5.0/7.0:
        player.mc.c2 = player.mc.c2 * (.5 + random())
    elif chance < 6.0/7.0:
        player.mc.c3 = player.mc.c3 * (.5 + random())
    else:
        player.mc.c4 = player.mc.c4 * (.5 + random())

def playNgames(player1, player2, n):
    wins = 0
    for x in range(0, n):
        print "playing game ", x, " of ", n
        board = MancalaBoard()
        board.hostGame(player1, player2)
        if board.hasWon(player1.num):
            wins += 1
    return wins / float(n)

def playNrounds(numPlayers, numRounds, numGames):
    players = [jge842(1, 4, 9), jge842(1, 4, 9)]
    players[0].mc.calculationTime = 5
    players[1].mc.calculationTime = 5
    winRatios = {}
    abprune = jge842(2, 3, 10)
    generation = 0
    while generation < numRounds:
        print "round ", generation + 1, "of ", numRounds
        while len(players) < numPlayers:
            chance = random()
            if chance < .5:
                newPlayer = deepcopy(players[0])
            else:
                newPlayer = deepcopy(players[1])
            adjustPlayer(newPlayer)
            players.append(newPlayer)
            winRatios[newPlayer] = 0
    
        for p in players:
            winRatios[p] = playNgames(p, abprune, numGames)

        toptwo = []
        for p in players:
            if len(toptwo) < 2:
                toptwo.append(p)
            else:
                for t in toptwo:
                    if winRatios[p] > winRatios[t]:
                        toptwo.append(p)
                        toptwo.remove(t)
                        break
        players = toptwo
        for p in players:
            mc = p.mc
            print (mc.interval1, mc.interval2, mc.interval3, mc.c1,
            mc.c2, mc.c3, mc.c4, winRatios[p])

        generation += 1
    first = players[0].mc
    second = players[1].mc
    return (first.interval1, first.interval2, first.interval3, first.c1,
            first.c2, first.c3, first.c4, winRatios[players[0]], second.interval1, second.interval2,
            second.interval3, second.c1, second.c2, second.c3, second.c4, winRatios[players[1]])

print playNrounds(4, 2, 2)
#First Generation

