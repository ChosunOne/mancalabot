# -*- coding: utf-8 -*-
from Player import Agent
from MancalaGUI import startGame

player1 = Agent(1, Agent.CUSTOM)
player2 = Agent(2, Agent.ABPRUNE)

startGame(player1, player2)
