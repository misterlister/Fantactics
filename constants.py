from enum import IntEnum

# Background colour for the game window
BG_COL = '#d9d9d9'
# Width and height of the game window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
# Width of divider lines
LINE_WIDTH = 2

# Number of pixels between a sprite and the border of its square
SPRITE_BUFFER = 8
# Size of images in the stats display window
STATS_IMAGE_SIZE = (2 * 64) + SPRITE_BUFFER
# Assets for error unpressed and pressed button
ERROR_UNPRESSED, ERROR_PRESSED = "Assets/Text/error_unpressed.png", "Assets/Text/error_pressed.png"
# Placeholder for empty sprites
EMPTY_SPRITE = "Assets/Text/empty.png"
# Default font
FONT = 'consolas'
# Default font size
DEFAULT_FONT_SIZE = 12

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

# Identifiers for unit sprites
class SpriteType:
    ARCHER1 = "Archer1"
    PEASANT1 = "Peasant1"
    SOLDIER1 = "Soldier1"
    SORCERER1 = "Sorcerer1"
    HEALER1 = "Healer1"
    ARCHMAGE1 = "Archmage1"
    ARCHER2 = "Archer2"
    PEASANT2 = "Peasant2"
    SOLDIER2 = "Soldier2"
    SORCERER2 = "Sorcerer2"
    HEALER2 = "Healer2"
    ARCHMAGE2 = "Archmage2"

# Damage multiplier for units initiating combat
FIRST_STRIKE_BOOST = 1.2
# Damage multiplier for ineffective attacks
POOR_EFFECT_MOD = 3/4
# Damage multiplier for effective attacks
STRONG_EFFECT_MOD = 4/3

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

