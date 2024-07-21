
from pygame import Rect


class Setting:
    SCREEN_RES = (1200, 750)
    FPS = 120
    TILE = 48
    TILEMAP = []
    PILL_SPEED = 4
    FRAME_PER_PILL_MOVE = 1
    HOME_NUMBER = 100
    PLAYER_SET = {
        'r':{'stop':1, 'home entry':51, 'dir':(1, 0, 6)},
        'g':{'stop':14, 'home entry':12, 'dir':(0, 1, 6)},
        'y':{'stop':27, 'home entry':25, 'dir':(-1, 0, 6)},
        'b':{'stop':40, 'home entry':38, 'dir':(0, -1, 6)},
    }
    @staticmethod
    def _get_tilemap(tile_size: int):
        tilemap = []
            
        for i in range(6):
            tilemap.append((i*tile_size, 6*tile_size))
        for i in range(6):
            tilemap.append((6*tile_size, (5-i)*tile_size))
        tilemap.append((7*tile_size, 0))
        for i in range(6):
            tilemap.append((8*tile_size, i*tile_size))
        for i in range(6):
            tilemap.append(((9+i)*tile_size, 6*tile_size))
        tilemap.append((14*tile_size, 7*tile_size))
        for i in range(6):
            tilemap.append(((14-i)*tile_size, 8*tile_size))
        for i in range(6):
            tilemap.append((8*tile_size, (9+i)*tile_size))
        tilemap.append((7*tile_size, 14*tile_size))
        for i in range(6):
            tilemap.append((6*tile_size, (14-i)*tile_size))
        for i in range(6):
            tilemap.append(((5-i)*tile_size, 8*tile_size))
        tilemap.append((0, 7*tile_size))
        return tilemap


    def __init__(self, board_rect: Rect):
        Setting.TILEMAP = Setting._get_tilemap(Setting.TILE)
        self.board_rect = board_rect
    
    def get_tile(self, tile_no: int, color: str):
        if tile_no >= Setting.HOME_NUMBER: 
            return self._get_home_tile(tile_no, color)
        tile_no = 0 if abs(tile_no)==52 else tile_no
        left, top = Setting.TILEMAP[tile_no]
        left = self.board_rect.left + left
        top = self.board_rect.top + top
        return left, top, tile_no
        
    def _get_home_tile(self, tile_no: int, color: str):
        entry_tile = Setting.PLAYER_SET[color]['home entry']
        home_tile_count = tile_no % Setting.HOME_NUMBER
        left, top, _ = self.get_tile(entry_tile, color)
        left = left + home_tile_count * Setting.PLAYER_SET[color]['dir'][0] * Setting.TILE
        top = top + home_tile_count * Setting.PLAYER_SET[color]['dir'][1] * Setting.TILE
        return left, top, tile_no
        
