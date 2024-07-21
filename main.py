import pygame
from pygame import Rect, display
import pygame.draw
import pygame.time
from classes import LudoBoard, Pill
from event_handler import check_events, check_game_events
from settings import Setting



pygame.init()
screen = display.set_mode(Setting.SCREEN_RES)
pygame.display.set_caption("Ludo Ludo")
fps_clock = pygame.time.Clock()
ludo_board = LudoBoard()
setting = Setting(ludo_board.get_rect())
pill = Pill('y', ludo_board.tile_board)
pill.set_position(*setting.get_tile(27, 'y'))

def game():
    screen.fill((0, 0, 0))
    ludo_board.show_board(screen)
    check_game_events(pill)
    pill.movement(setting)
    pill.show_pill(screen)
    display.flip()
    fps_clock.tick(Setting.FPS)


    # print(ludo_board.get_rect().topleft)
    # for x, y in Setting.TILEMAP:
    #     r = Rect(x+ludo_board.get_rect().left, y+ludo_board.get_rect().top, Setting.TILE, Setting.TILE)
    #     pygame.draw.rect(screen, (0,0,255), r, 10)


if __name__=="__main__":
    while True:
        # screen.fill((0, 0, 0))
        # check_events()
        game()
        # display.flip()
        # fps_clock.tick(Setting.FPS)