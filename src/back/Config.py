"""File contains constants"""

import pygame
from src.back.Character import *

# globals
MAPPA = None
PLAYER = None

# chars for map
CHAR_FOR_PATH = 'P'
CHAR_FOR_EMPTY = 'E'
CHAR_FOR_BOARD = 'B'
CHAR_FOR_FLOOR = 'P'
CHAR_FOR_CURRENT_POS = 'C'
CHAR_FOR_EXIT = 'X'
CHAR_FOR_ANSWER = 'A'

# num of pngs
NUM_OF_PNGS_FOR_FLOOR = 14
NUM_OF_SPRITES_FOR_ATTACK = 5
NUM_OF_SPRITES_FOR_DEATH_ANIMATION = 14

FREAQ_OF_DEATH_ANIMATION = 60
COOLDOWN_FOR_ATTACK = 50

CHARS_FOR_FLOORS = [CHAR_FOR_FLOOR + ' ' + str(index) for index in range(1, NUM_OF_PNGS_FOR_FLOOR + 1)]

# sizes of rectangles
SIZE_OF_DISPLAY = [1920, 1080]
SIZE_OF_UNSCOPED_MINIMAP = [450, 450]
SIZE_OF_SCOPED_MINIMAP = [SIZE_OF_DISPLAY[0] / 2, SIZE_OF_DISPLAY[1] / 2]
SIZE_OF_MINIMAP = SIZE_OF_UNSCOPED_MINIMAP
SIZE_OF_MAP = [8, 8]
SIZE_OF_MENUS = [SIZE_OF_DISPLAY[0] / 2, SIZE_OF_DISPLAY[1] / 2]
SIZE_OF_MAIN_MENU = SIZE_OF_DISPLAY

# sizes of tiles
SIZE_OF_CHARACTER = 48
SIZE_OF_TILE = 96

# positions
POSITION_OF_MINIMAP = [SIZE_OF_DISPLAY[0] - SIZE_OF_MINIMAP[0], 0]

# character characteristic
SPEED_OF_CHARACTER = 7
SPAWN_POSITION = [SIZE_OF_DISPLAY[0] // 2, SIZE_OF_DISPLAY[1] // 2]

# path to files
PATH_TO_CHARACTER_PNG = "images/tiles_for_chars/"
PATH_TO_FLOOR_PNG = "images/tiles_for_map/floor/sprite_"
PATH_TO_EMPTY_TILE_PNG = "images/tiles_for_map/back_ground/sprite_078.png"
PATH_TO_EXIT_PNG = "images/tiles_for_map/exit/sprite_038.png"
PATH_TO_SIDE_ATTACK = "images/tiles_for_animations/tiles_for_side_attack/sprite_"
PATH_TO_UPPER_ATTACK = "images/tiles_for_animations/tiles_for_upper_attack/sprite_"
PATH_FOR_DEATH_ANIMATION = "images/tiles_for_effects/animation_of_death/sprite_"
FILE_WITH_IMAGES_EXTENSION = '.png'

# specific colors
COLOR_FOR_BACKGROUND = (37, 19, 26)
COLOR_FOR_CURRENT_POSITION = (51, 255, 0)
COLOR_FOR_ANSWER_TILES = (255, 255, 0)
COLOR_FOR_HEALTH_BAR = (210, 0, 0)
COLOR_FOR_EMPTY_HEALTH_BAR = (92, 0, 0)

# specific constants
LENGTH_OF_PATHS = 4
FRAMES_PER_SEC = 60
DEEP_OF_RECURSION = 10000000

MAX_SIZE_OF_NAME_OF_FILE = 20
SEED_FOR_TEST = 12
DEFAULT_LENGTH_FOR_DFS = 1000000

# names of chars
KNIGHT_NAME = 'Knight'

# preferences for menus
SET_WITH_DIFFICULTIES = [('I’m Too Young to Die', 1), ('Hurt Me Plenty', 2), ('Ultra Violence', 3), ('Nightmare', 4),
                         ('Just A Psycho', 5)]
SET_WITH_ALGOS = [('DFS', 'DFS'), ('Prima', 'Prima')]
SET_WITH_SIZES = [('Tiny [16, 16]', [16, 16]), ('Classic [32, 32]', [32, 32]), ('Large [64, 64]', [64, 64]),
                  ('Huge [128, 128]', [128, 128])]
SET_WITH_CHARACTERS = [(KNIGHT_NAME, Knight)]
LENGTHS_PATHS_ACCORDING_TO_DIFFICULTY = [0, 7, 4, 4, 1, 1]

# strings for states
START_MENU_STATE = 'start_menu'
IN_GAME_MENU_STATE = 'in_game_menu'
END_GAME_MENU_STATE = 'end_menu'
IN_GAME_STATE = 'in_game'
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

# cases
STATE = START_MENU_STATE
DIFFICULTY = 1
CHARACTER = 'necromancer'
ALGO_FOR_GENERATION = 'DFS'
DFS = 'DFS'
PRIMA = 'Prima'
RUNNING = True

# places for in-game ui
SIZE_OF_SETTINGS_BUTTON = [100, 50]
PLACE_OF_SETTINGS_BUTTON = [10, 10]
SIZE_OF_RESTART_BUTTON = [SIZE_OF_DISPLAY[0] // 10, SIZE_OF_DISPLAY[1] // 10]
PLACE_OF_RESTART_BUTTON = [SIZE_OF_DISPLAY[0] // 2 - SIZE_OF_RESTART_BUTTON[0] // 2,
                           SIZE_OF_DISPLAY[1] // 2 - SIZE_OF_RESTART_BUTTON[1] // 2]

POSITION_OF_HEALTH_BAR = [SIZE_OF_DISPLAY[0] // 50, SIZE_OF_DISPLAY[1] // 30]
PIXELS_PER_HEALTH_POINT = SIZE_OF_DISPLAY[0] // 320
WIDTH_OF_HEALTH_BAR = SIZE_OF_DISPLAY[1] // 30

SIZE_OF_SHOW_ANSWER_BUTTON = [160, 50]
PLACE_OF_SHOW_ANSWER_BUTTON = [SIZE_OF_DISPLAY[0] // 2 - SIZE_OF_SHOW_ANSWER_BUTTON[0] // 2, 10]

# strings for UI
CAPTION = 'Maze Enjoyer'
WELCOME_CONDITION_STRING = 'Welcome'
PLAY_CONDITION_STRING = 'Play'
WIN_CONDITION_STRING = 'You Won'
RETRY_CONDITION_STRING = 'Retry'
QUIT_CONDITION_STRING = 'Quit'
SETTINGS_CONDITION_STRING = 'Settings'
BACK_CONDITION_STRING = 'Back'
DIFFICULTY_SELECTION_STRING = 'Difficulty:'
SIZE_SELECTION_STRING = 'Size:'
ALGORITHM_CONDITION_STRING = 'Algorithm for generator:'
MENU_CONDITION_STRING = 'Menu'
RESUME_CONDITION_STRING = 'Resume'
CHARACTER_SELECTION_STRING = 'Character:'
ANSWER_BUTTON_STRING = 'Show Answer'
SAVE_MAZE_STRING = 'Save'
NAME_MAZE_STRING = 'Name of the save:'
DEFAULT_NAME_FOR_SAVE = 'New_Save'
LOAD_STRING = 'Load'
CHOOSE_FILE_STRING = 'Choose file:'
PICK_SERVER_STRING = 'Pick a server'
CONNECT_BUTTON_STRING = 'Connect'

LOG_IN_STRING = 'Log in'
REGISTRATION_STRING = 'Register an account'

USER_NM_INPUT = 'User name/email address: '
NICK_NAME_INPUT = 'Nickname: '
PASSWORD_INPUT = 'Password: '

WRONG_LOG_IN = 'Wrong user name or password'
WRONG_REGISTER = 'This user name is used'
WRONG_SERVER_SELECTION = 'You did not choose a server!'

# main menu
POSITION_OF_PROFILE_BUTTON = (0, 0)

# characteristics of characters
KNIGHT_MOVEMENT_SPEED = 7
KNIGHT_HEALTH = 50
KNIGHT_SIZE = 48
KNIGHT_ATTACK_SPEED = 35
KNIGHT_DAMAGE = 8

# id for sprites
SPRITE_ID_FOR_ATTACK = 'A'
SPRITE_ID_FOR_LEFT_ATTACK = 'A' + LEFT
SPRITE_ID_FOR_RIGHT_ATTACK = 'A' + RIGHT
SPRITE_ID_FOR_Up_ATTACK = 'A' + UP
SPRITE_ID_FOR_DOWN_ATTACK = 'A' + DOWN
SPRITE_ID_FOR_DEATH = 'DEATH'
