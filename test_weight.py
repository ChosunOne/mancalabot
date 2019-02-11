import numpy as np
from MancalaBoard import *
from Player import *

print "Test AI of Different Heuristic Weights"
file = open("test_weight", "w+")

a = np.arange(0, 1.1, 0.1)
for i in a:
    p1 = MancalaPlayer(1, 4, 9, i)
    count_first_win = 0
    count_first_lose = 0
    count_first_tie = 0
    count_second_win = 0
    count_second_lose = 0
    count_second_tie = 0
    for j in a:
        if i != j:
            p2 = MancalaPlayer(2, 4, 9, j)
            MB = MancalaBoard()
            winner = MB.hostGame(p1, p2)
            if winner == 1:
                count_first_win += 1
            elif winner == 2:
                count_first_lose += 1
            else:
                count_first_tie += 1
            winner = MB.hostGame(p2, p1)
            if winner == 2:
                count_second_win += 1
            elif winner == 1:
                count_second_lose += 1
            else:
                count_second_tie += 1
    count_first_all = count_first_win + count_first_lose + count_first_tie
    rate_first_win = count_first_win / count_first_all
    rate_first_tie = count_first_tie / count_first_all
    file.write("h1weight: "+str(i)+" rate_first_win: " + str(rate_first_win) + " rate_first_tie: " + str(rate_first_tie) + "\n")
    count_second_all = count_second_win + count_second_lose + count_second_tie
    rate_second_win = count_second_win / count_second_all
    rate_second_tie = count_second_tie / count_second_all
    file.write("h1weight: "+str(i)+" rate_second_win: " + str(rate_second_win) + " rate_second_tie: " + str(rate_second_tie) + "\n")

file.close()
