from random import randint
import pygame
import pygame.draw
import pygame.image
import pygame.surface
import pygame.transform
from settings import Setting



class LudoBoard:
    IMG_PATH = "asset\\board.png"
    def __init__(self):
        self.img = pygame.image.load(LudoBoard.IMG_PATH)
        self.rect = self.img.get_rect()
        self.rect.center = Setting.SCREEN_RES[0]/2 + 3*Setting.TILE, Setting.SCREEN_RES[1]/2
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
        self.activity = 0 #-1 for completion, 0 for not active, 1 for active
    
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
    
    def mark_pill(self, screen: pygame.Surface):
        pygame.draw.rect(screen, Setting.COLOR[self.color], self.rect, 2, 1)
    
    def is_pickable(self, dice_num: int)->bool:
        if self.curr_tile < 0:
            return False
        if self.curr_tile >= Setting.HOME_NUMBER:
            if (self.curr_tile % Setting.HOME_NUMBER)+dice_num > Setting.PLAYER_SET[self.color]['dir'][2]:
                return False
        return True

    
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
        self.pills = [Pill(color, None) for _ in range(Setting.PILL_PER_PLAYER)]
        self.current_pill = 0
        self.pickable_pills: list[int] = []
        self._set_pill_positions()
    
    def _set_pill_positions(self):
        positions = [self.rest_rect.topleft, self.rest_rect.topright, self.rest_rect.bottomleft, self.rest_rect.bottomright]
        for i in range(Setting.PILL_PER_PLAYER):
            self.pills[i].set_position(*positions[i%4])
    
    def show_player(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0,0,0), self.rest_rect, 20)
    
    def find_pickable_pills(self, dice_num:int):
        self.pickable_pills.clear()
        for i in range(len(self.pills)):
            if self.pills[i].is_pickable(dice_num):
                self.pickable_pills.append(i)
    
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
    
    def mark_player(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0,0,0), self.area_rect, Setting.PLAYER_GLOW_WIDTH_LIM//2+2, 5)
        pygame.draw.rect(screen, Setting.COLOR[self.color], self.area_rect, Setting.PLAYER_GLOW_WIDTH_LIM//2, 5)
        
    
    def show_pills(self, screen: pygame.Surface):
        for pill in self.pills:
            pill.show_pill(screen)
    
    def mark_all_pills(self, screen: pygame.Surface):
        for pill in self.pills:
            pill.mark_pill(screen)
        self.pills[self.current_pill].glow_pill(screen)
    
    def toggle_pills(active:int = True):
        #Toggle between only active or all pills
        pass
        



class Ludo:
    def __init__(self, screen: pygame.Surface, player_count:int=2):
        self.screen = screen
        self.ludo_board = LudoBoard()
        self.setting = Setting(self.ludo_board.get_rect())
        self.players = [Player(c, self.setting) for c in Setting.PLAYER_NUMBERS[player_count]]
        self.current_player = 0
        self.pills:list[Pill] = []
        self.dice = Dice()
        self.stage = 1
        self.frame = 1
        for player in self.players:
            self.pills += player.pills
        
    def view_board(self):
        self.ludo_board.show_board(self.screen)
        # for player in self.players:
        #     player.glow_player(self.screen)
        for pill in self.pills:
            pill.show_pill(self.screen)
        self.dice.show_dice(self.screen)
    
    def view_operating_board(self):
        if self.stage == 1:
            self.wait_to_roll()
        if self.stage == 2:
            self.roll_the_dice()
        if self.stage == 3:
            self.choose_pill()
        if self.stage == 7:
            self.switch_player()

    def switch_player(self):
        self.frame += 1
        self.wait_to_roll(False, False)
        if (self.frame % int(Setting.PLAYER_SWITCHING_DELAY * Setting.FPS))==0:
            self.current_player += 1
            self.current_player = self.current_player % len(self.players)
            self.stage = 1
            self.frame = 1
    
    def wait_to_roll(self, player_glow:bool=True, blinking:bool=True):
        if player_glow==True:
            self.players[self.current_player].glow_player(self.screen)
        else: self.players[self.current_player].mark_player(self.screen)
        if blinking==True:
            self.dice.blinking()
    
    def roll_the_dice(self):
        is_rolled = self.dice.roll()
        if is_rolled:
            self.players[self.current_player].find_pickable_pills(self.dice.current_dice)
            self.stage = 3
    
    def choose_pill(self):
        if len(self.players[self.current_player].pickable_pills) == 0:
            self.stage = 7
            return
        self.players[self.current_player].mark_all_pills(self.screen)
    
    def spacebar_action(self):
        if self.stage == 1:
            self.dice.frames=0 # resetting the dice frame for next animation
            self.stage = 2
    
    def tabkey_action(self):
        if self.stage == 3:
            pass
            

        



class Dice:
    LOCATION = "asset\\dice\\"
    def __init__(self):
        dices = [pygame.image.load(Dice.LOCATION+str(i)+".png") for i in range(1,7)]
        self.dices = [pygame.transform.rotozoom(dice, 0, 0.75) for dice in dices]
        pots = [pygame.image.load(Dice.LOCATION+'pot'+str(i)+".png") for i in range(1,3)]
        self.pots = [pygame.transform.rotozoom(pot, 0, 0.75) for pot in pots]
        self.pot_rect = self.pots[0].get_rect()
        self.dice_rect = self.dices[0].get_rect()
        self.pot_rect.center = self.pot_rect.width, Setting.SCREEN_RES[1]//2
        self.dice_rect.center = self.pot_rect.center
        self.current_dice = 5
        self.frames = 0
        self.curr_pot = 0
    
    def show_dice(self, screen:pygame.Surface):
        screen.blit(self.pots[self.curr_pot], self.pot_rect)
        screen.blit(self.dices[self.current_dice-1], self.dice_rect)
    
    def blinking(self, speed:int=1):
        if self.frames % int(Setting.FRAME_PER_DICE_BLINK/speed) == 0:
            self.curr_pot = (self.curr_pot+1)%len(self.pots)
            # self.frames=1
        if speed==1:
            self.frames += 1
    
    def roll(self)->bool:
        if self.frames % Setting.FRAME_PER_DICE_ROLL_ANIM == 0:
            self.current_dice = (self.current_dice+1) % len(self.dices)
        self.frames += 1
        self.blinking(Setting.DICE_BLINKING_SPEED_WHILE_ROLLING)
        if self.frames >= int(Setting.TIME_PER_DICE_ROLL * Setting.FPS):
            self.current_dice = randint(1, 6)
            self.frames = 0
            self.curr_pot = 0
            return True
        return False
    