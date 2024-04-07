from enum import IntEnum

# Background colour for the game window
BG_COL = '#a9a9a9'
# Width and height of the game window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
# Width of divider lines
LINE_WIDTH = 3

# Number of pixels between a sprite and the border of its square
SPRITE_BUFFER = 8
# Size of images in the stats display window
STATS_IMAGE_SIZE = (1.5 * 64)
# Assets for error unpressed and pressed button
ERROR_UNPRESSED, ERROR_PRESSED = "Assets/Text/error_unpressed.png", "Assets/Text/error_pressed.png"
# Placeholder for empty sprites
EMPTY_SPRITE = "Assets/Text/empty.png"
# Default font
FONT = 'consolas'
# Default font size
DEFAULT_FONT_SIZE = 11

UI_BG_COLOUR = '#5d4037'
DEFAULT_TEXT_COLOUR = '#ffffff'
BORDER_WIDTH = 4
PANEL_WIDTH, PANEL_HEIGHT = 320, 720 
CONTROL_PANEL_HEIGHT = 80

# Size of the game squares
DEFAULT_SQUARE_SIZE = 64 + SPRITE_BUFFER
# Space between the game square line and the selection squares
SELECTION_BUFFER = 3
# Size of selection squares
SELECTION_SQUARE = DEFAULT_SQUARE_SIZE - SELECTION_BUFFER
# Number of game rows and columns
BOARD_ROWS = 8
BOARD_COLS = 8
# Pixel width and height of the board
BOARD_WIDTH = DEFAULT_SQUARE_SIZE * BOARD_COLS
BOARD_HEIGHT = DEFAULT_SQUARE_SIZE * BOARD_ROWS
# X and Y coordinates of the top left of the game board
DEFAULT_X_POS = ((WINDOW_WIDTH - BOARD_WIDTH) // 2)
DEFAULT_Y_POS = ((WINDOW_HEIGHT - BOARD_HEIGHT) // 4)

MOVE_COL = "green"
ATTACK_COL = "red"
SELECT_COL = "blue"
ACTION_COL = "purple"
ABILITY_COL = "yellow"

# Identifiers for unit sprites
class SpriteType:
    ARCHER1 = "Archer1"
    PEASANT1 = "Peasant1"
    SOLDIER1 = "Soldier1"
    SORCERER1 = "Sorcerer1"
    CAVALRY1 = "Cavalry1"
    HEALER1 = "Healer1"
    ARCHMAGE1 = "Archmage1"
    GENERAL1 = "General1"
    ARCHER2 = "Archer2"
    PEASANT2 = "Peasant2"
    SOLDIER2 = "Soldier2"
    SORCERER2 = "Sorcerer2"
    CAVALRY2 = "Cavalry2"
    HEALER2 = "Healer2"
    ARCHMAGE2 = "Archmage2"
    GENERAL2 = "General2"
    
class TerrainType:
    PLAINS = "plains"
    FOREST = "forest"
    FOREST_E = "forest_e"
    FOREST_ES = "forest_es"
    FOREST_ESW = "forest_esw"
    FOREST_EW = "forest_ew"
    FOREST_N = "forest_n"
    FOREST_NE = "forest_ne"
    FOREST_NES = "forest_nes"
    FOREST_NESW = "forest_nesw"
    FOREST_NEW = "forest_new"
    FOREST_NS = "forest_ns"
    FOREST_NSW = "forest_nsw"
    FOREST_NW = "forest_nw"
    FOREST_S = "forest_s"
    FOREST_SW = "forest_sw"
    FOREST_W = "forest_w"
    FORTRESS = "fortress"
    PATH_E = "path_e"
    PATH_ES = "path_es"
    PATH_ESW = "path_esw"
    PATH_EW = "path_ew"
    PATH_N = "path_n"
    PATH_NE = "path_ne"
    PATH_NES = "path_nes"
    PATH_NESW = "path_nesw"
    PATH_NEW = "path_new"
    PATH_NS = "path_ns"
    PATH_NSW = "path_nsw"
    PATH_NW = "path_nw"
    PATH_S = "path_s"
    PATH_SW = "path_sw"
    PATH_W = "path_w"
    PATH = "path"

# Damage multiplier for units initiating combat
FIRST_STRIKE_BOOST = 1.2
# Damage multiplier for ineffective attacks
POOR_EFFECT_MOD = 3/4
# Damage multiplier for effective attacks
STRONG_EFFECT_MOD = 4/3

# Modifier bonus for aura abilities
AURA_MOD = 1
# Range for aura abilities
AURA_RANGE = 2

class Direction(IntEnum):
    UP = 1
    LEFT = 2
    RIGHT = 3
    DOWN = 4

# Enums for attack damage types
class DamageType(IntEnum):
    SLASH = 1
    PIERCE = 2
    BLUDGEON = 3
    MAGIC = 4

# Enums for armour types
class ArmourType(IntEnum):
    ROBES = 1
    PADDED = 2
    CHAIN = 3
    PLATE = 4

# Enums for damage type/armour type effectiveness
class Effect(IntEnum):
    POOR = 1
    NEUTRAL = 2
    STRONG = 3

# Enums for unit movement speed
class MoveSpeed(IntEnum):
    SLOW = 2
    MED = 3
    FAST = 4

# Enums for unit movement types
class MoveType(IntEnum):
    FOOT = 1
    HORSE = 2
    FLY = 3

class ActionType(IntEnum):
    MOVE = 1
    ATTACK = 2
    ABILITY = 3

class TargetType(IntEnum):
    ITSELF = 1
    ALLY = 2
    ENEMY = 3
    NONE = 4

TARGET_ENEMIES = {
    TargetType.ITSELF: False,
    TargetType.ALLY: False,
    TargetType.ENEMY: True,
    TargetType.NONE: False
}

TARGET_MOVE = {
    TargetType.ITSELF: True,
    TargetType.ALLY: False,
    TargetType.ENEMY: False,
    TargetType.NONE: True
}

TARGET_ALLIES = {
    TargetType.ITSELF: False,
    TargetType.ALLY: True,
    TargetType.ENEMY: False,
    TargetType.NONE: False
}

TARGET_SELF = {
    TargetType.ITSELF: True,
    TargetType.ALLY: False,
    TargetType.ENEMY: False,
    TargetType.NONE: False
}

TARGET_OTHERS = {
    TargetType.ITSELF: False,
    TargetType.ALLY: True,
    TargetType.ENEMY: True,
    TargetType.NONE: False
}

TARGET_ALL = {
    TargetType.ITSELF: True,
    TargetType.ALLY: True,
    TargetType.ENEMY: True,
    TargetType.NONE: True
}

TARGET_NONE = {
    TargetType.ITSELF: False,
    TargetType.ALLY: False,
    TargetType.ENEMY: False,
    TargetType.NONE: False
}

TARGET_SELF_ENEMIES = {
    TargetType.ITSELF: True,
    TargetType.ALLY: False,
    TargetType.ENEMY: True,
    TargetType.NONE: False
}

# Maximum length of message and size of message buffer
MAX_MESSAGE_SIZE = 256

#Receiver timeout length in seconds
TIMEOUT_LENGTH = 2

#IP Address of Host:
IP = "localhost"

#Port used for server listen socket.
PORT = 5000