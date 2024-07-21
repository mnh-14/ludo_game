import pygame
import sys

import pygame.event
from settings import Setting
from classes import LudoBoard, Pill

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def check_game_events(pill: Pill):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pill.reamining_move += 5