# -*- coding: utf-8 -*-
from Player import Agent
from MancalaGUI import startGame

player1 = Agent(1, 4)
player2 = Agent(2, 3)

startGame(player1, player2)
