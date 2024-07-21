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
        self.movement_direction = 1
        self.glow_direction = -1
        self.glow_width = Setting.PILL_GLOW_WIDTH_LIM
        self.glow_frame = 0
    
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
    
    def glow_pill(self, screen: pygame.Surface):
        if self.glow_frame % Setting.FRAME_PER_PILL_GLOW != 0:
            self.glow_frame += 1
            # print("Pill grow frame", self.glow_frame)
        else: 
            self.glow_width += self.glow_direction
            self.glow_frame = 1
            if self.glow_width > Setting.PILL_GLOW_WIDTH_LIM or self.glow_width < 2:
                self.glow_direction *= -1
        pygame.draw.rect(screen, (0,0,0), self.rect, self.glow_width+1, 2)
        pygame.draw.rect(screen, Setting.COLOR[self.color], self.rect, self.glow_width, 2)
    
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
            return
        if self.movement_direction > 0 and self.curr_tile == Setting.PLAYER_SET[self.color]['home entry']:
            self.curr_tile = Setting.HOME_NUMBER

        left, top, tile_no = setting.get_tile(self.curr_tile+self.movement_direction, self.color)
        self._pure_move(left, top)
        if self.rect.left == left and self.rect.top == top:
            self.reamining_move -= 1
            self.curr_tile = tile_no



class Player:
    def __init__(self, color:str, setting: Setting) -> None:
        left, top = Setting.PLAYER_SET[color]['rest']
        left, top = left*Setting.TILE + setting.board_rect.left, top*Setting.TILE + setting.board_rect.top
        self.state = 0
        self.color = color
        self.glow_frame = 1
        self.glow_width = Setting.PLAYER_GLOW_WIDTH_LIM
        self.glow_direction = -1
        self.rest_rect = pygame.Rect(left, top, 2*Setting.TILE, 2*Setting.TILE)
        left, top = Setting.PLAYER_SET[color]['area']
        left, top = left*Setting.TILE + setting.board_rect.left, top*Setting.TILE + setting.board_rect.top
        self.area_rect = pygame.Rect(left, top, 6*Setting.TILE, 6*Setting.TILE)
        self.pills = [Pill(color, None) for _ in range(4)]
        self._set_pill_positions()
    
    def _set_pill_positions(self):
        positions = [self.rest_rect.topleft, self.rest_rect.topright, self.rest_rect.bottomleft, self.rest_rect.bottomright]
        for i in range(4):
            self.pills[i].set_position(*positions[i])
    
    def show_player(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0,0,0), self.rest_rect, 20)
    
    def glow_player(self, screen: pygame.Surface):
        if self.glow_frame % Setting.FRAME_PER_PLAYER_GLOW != 0:
            self.glow_frame += 1
        else:
            self.glow_width += self.glow_direction
            self.glow_frame = 1
            if self.glow_width > Setting.PLAYER_GLOW_WIDTH_LIM or self.glow_width < 5:
                self.glow_direction *= -1
        pygame.draw.rect(screen, (0,0,0), self.area_rect, self.glow_width+2, 5)
        pygame.draw.rect(screen, Setting.COLOR[self.color], self.area_rect, self.glow_width, 5)
    
    def show_pills(self, screen: pygame.Surface):
        for pill in self.pills:
            pill.show_pill(screen)



class Ludo:
    def __init__(self, screen: pygame.Surface, player_count:int=2):
        self.screen = screen
        self.ludo_board = LudoBoard()
        self.setting = Setting(self.ludo_board.get_rect())
        self.players = [Player(c, self.setting) for c in Setting.PLAYER_NUMBERS[player_count]]
        self.current_player = 0
        self.pills:list[Pill] = []
        for player in self.players:
            self.pills += player.pills
        
    def view_board(self):
        self.ludo_board.show_board(self.screen)
        for player in self.players:
            player.glow_player(self.screen)
        for pill in self.pills:
            pill.show_pill(self.screen)
            pill.glow_pill(self.screen)



class Dice:
    LOCATION = "asset\\dice\\"
    def __init__(self):
        self.images = [pygame.image.load(Dice.LOCATION+str(i)+".png") for i in range(1,7)]
        self.pots = [pygame.image.load(Dice.LOCATION+'pot'+str(i)+".png") for i in range(1,7)]