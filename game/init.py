import pygame

import sys
import os

# Obtenez le chemin absolu du dossier racine
root_path = os.path.dirname(os.path.abspath(__file__))

from first_game.game import Game

# Ajoutez le chemin du dossier racine à sys.path
sys.path.insert(0, root_path)

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()