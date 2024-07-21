import pygame
import pygame.draw
import pygame.image
import pygame.surface
from settings import Setting



class LudoBoard:
    IMG_PATH = "asset\\board.png"
    def __init__(self):
        self.img = pygame.image.load(LudoBoard.IMG_PATH)
        self.rect = self.img.get_rect()
        self.rect.center = Setting.SCREEN_RES[0]/2, Setting.SCREEN_RES[1]/2
        self.tile_board = [0 for _ in range(52)]
    
    def show_board(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (255,255,255), self.rect)
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, 4)
    
    def get_rect(self):
        return self.rect


class Pill:
    PILLS = {'r':"red", 'g':"green", 'b':"blue", 'y':"yellow"}
    def __init__(self, color: str, tileboard: list[int]):
        self.curr_tile = -1
        self.color = color
        self.rect = pygame.Rect(0, 0, Setting.TILE, Setting.TILE)
        self.img = pygame.image.load("asset\\"+Pill.PILLS[color]+"_pill.png")
        self.img_rect = self.img.get_rect()
        self.temp_img = self.img.copy()
        self.reamining_move = 0
        self.movement_frame = 0
    
    def set_position(self, left, top, tile_no=-1):
        self.rect.top = top
        self.rect.left = left
        self.curr_tile = tile_no
        self.img_rect.center = self.rect.center
    
    def show_pill(self, screen: pygame.Surface, modified: bool=False):
        self.img_rect.center = self.rect.center
        if modified:
            screen.blit(self.temp_img, self.img_rect)
        else:
            screen.blit(self.img, self.img_rect)
    
    def _pure_move(self, left, top):
        diff = left - self.rect.left, top - self.rect.top
        dx = diff[0]/abs(diff[0]) if diff[0]!=0 else 0
        dy = diff[1]/abs(diff[1]) if diff[1]!=0 else 0
        
        if Setting.PILL_SPEED < abs(diff[0]) and diff[0]!=0:
            self.rect.left += dx * Setting.PILL_SPEED
        elif diff[0]!=0:
            self.rect.left = left
        if Setting.PILL_SPEED < abs(diff[1]) and diff[1]!=0:
            self.rect.top += dy * Setting.PILL_SPEED
        elif diff[1]!=0:
            self.rect.top = top
            
    def movement(self, setting: Setting):
        if self.reamining_move == 0:
            self.movement_frame = 0
            return
        if self.movement_frame % Setting.FRAME_PER_PILL_MOVE != 0:
            self.movement_frame += 1
            # print("Increasing frame count")
            return

        left, top, tile_no = setting.get_tile(self.curr_tile+1, self.color)
        self._pure_move(left, top)
        if self.rect.left == left and self.rect.top == top:
            self.reamining_move -= 1
            self.curr_tile = tile_no
        # if self.curr_tile == len(Setting.TILEMAP):
        #     self.curr_tile = 0

