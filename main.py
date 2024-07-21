import pygame
from pygame import Rect, display
import pygame.draw
import pygame.time
from classes import Ludo, LudoBoard, Pill, Player
from event_handler import check_events, check_game_events
from settings import Setting



pygame.init()
screen = display.set_mode(Setting.SCREEN_RES)
pygame.display.set_caption("Ludo Ludo")
fps_clock = pygame.time.Clock()

ludo = Ludo(screen, 4)


def gameplay():
    screen.fill((0,0,0))
    ludo.view_board()
    check_game_events(ludo)
    display.flip()
    fps_clock.tick(Setting.FPS)


if __name__=="__main__":
    while True:
        # screen.fill((0, 0, 0))
        # check_events()
        gameplay()
        # display.flip()
        # fps_clock.tick(Setting.FPS)