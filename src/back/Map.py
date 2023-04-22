"""File contains map class"""

import pygame
import random
import time
import sys
from src.back.MapGenerator import *
from src.back.Config import *
import src.back.Config
import src.back.Algorithms as Algo
import src.front.Menus

random.seed(time.time())
# random.seed(SEED_FOR_TEST)

list_with_floor = []

image_for_empty = pygame.image.load(PATH_TO_EMPTY_TILE_PNG)
image_for_empty = pygame.transform.scale(image_for_empty, (SIZE_OF_TILE, SIZE_OF_TILE))

image_for_exit = pygame.image.load(PATH_TO_EXIT_PNG)
image_for_exit = pygame.transform.scale(image_for_exit, (SIZE_OF_TILE, SIZE_OF_TILE))

generated_floor = {}


def SetImage(path, number):
    """this function gives unpacked image"""

    result = pygame.image.load(path + str(number) + FILE_WITH_IMAGES_EXTENSION)
    result = pygame.transform.scale(result, (SIZE_OF_TILE, SIZE_OF_TILE))
    return result


def SetTiles():
    """this function set all sprites of the game"""

    for i in range(1, NUM_OF_PNGS_FOR_FLOOR + 1):
        list_with_floor.append(SetImage(PATH_TO_FLOOR_PNG, i))


class Map:
    def __init__(self, matrix_with_map=None,
                 tiles_for_current_room={}, visited_tiles={},
                 matrix_with_visited=None,
                 global_map_position=[0, 0], current_room_position=[0, 0], answer=[]):
        """initialize map"""

        SetTiles()

        self.matrix_with_map = matrix_with_map
        self.matrix_with_visited = matrix_with_visited
        if self.matrix_with_map is None:
            algorithm = None
            if src.back.Config.ALGO_FOR_GENERATION == 'DFS':
                algorithm = Algo.DFSAlgo()
            elif src.back.Config.ALGO_FOR_GENERATION == 'Prima':
                algorithm = Algo.PrimaAlgo()
            self.matrix_with_map = MapGenerator.GenerateMaze(src.back.Config.SIZE_OF_MAP, algorithm)

        if self.matrix_with_visited is None:
            self.matrix_with_visited = MapGenerator.GetClearMap(src.back.Config.SIZE_OF_MAP)

        self.mappa = pygame.Surface(
            (len(self.matrix_with_map) * SIZE_OF_TILE, len(self.matrix_with_map[0]) * SIZE_OF_TILE))

        self.tiles_for_current_room = tiles_for_current_room
        self.current_room = pygame.Surface((0, 0))

        self.visited_tiles = visited_tiles
        self.visited_mappa = pygame.Surface(
            (len(self.matrix_with_map) * SIZE_OF_TILE, len(self.matrix_with_map[0]) * SIZE_OF_TILE))
        self.BlitSpecificOnMap(self.visited_mappa, self.visited_tiles)

        self.global_map_position = global_map_position
        self.current_room_position = current_room_position

        self.dfs = DFSAlgo()
        self.bfs = BFSAlgo()

        self.answer = answer

        self.SetTilesOnMap(self.mappa, self.matrix_with_map, (0, 0))

    def BlitSpecificMap(self, list_with_map):
        """blit specific matrix with tiles on the current map"""

        left_upper_corner = (
            min(list_with_map, key=lambda item: item[0][0])[0][0],
            min(list_with_map, key=lambda item: item[0][1])[0][1])
        right_down_corner = (
            max(list_with_map, key=lambda item: item[0][0])[0][0],
            max(list_with_map, key=lambda item: item[0][1])[0][1])
        width = right_down_corner[0] - left_upper_corner[0] + 1
        height = right_down_corner[1] - left_upper_corner[1] + 1

        self.current_room = pygame.Surface((width * SIZE_OF_TILE, height * SIZE_OF_TILE))

        matrix_with_map = []
        for i in range(width):
            intermediate = []
            for j in range(height):
                intermediate.append(CHAR_FOR_EMPTY)
            matrix_with_map.append(intermediate)

        for tile in list_with_map:
            matrix_with_map[tile[0][0] - left_upper_corner[0]][tile[0][1] - left_upper_corner[1]] = tile[1]
        self.SetTilesOnMap(self.current_room, matrix_with_map, left_upper_corner)
        return left_upper_corner

    @staticmethod
    def SetTilesOnMap(surface, matrix, left_corner):
        """blit map according to the matrix and position of left corner relative to left corner of the main matrix"""

        x, y = 0, 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] in [CHAR_FOR_PATH]:
                    if (i + left_corner[0], j + left_corner[1]) in generated_floor:
                        surface.blit(generated_floor[(i + left_corner[0], j + left_corner[1])], (x, y))
                    else:
                        generated_floor[(i + left_corner[0], j + left_corner[1])] = random.choice(list_with_floor)
                        surface.blit(generated_floor[(i + left_corner[0], j + left_corner[1])], (x, y))
                elif matrix[i][j] in [CHAR_FOR_EXIT]:
                    surface.blit(image_for_exit, (x, y))
                elif matrix[i][j] in [CHAR_FOR_ANSWER]:
                    pygame.draw.rect(surface, color=COLOR_FOR_ANSWER_TILES, rect=[x, y, SIZE_OF_TILE, SIZE_OF_TILE])
                else:
                    surface.blit(image_for_empty, (x, y))
                y += SIZE_OF_TILE
            x += SIZE_OF_TILE
            y = 0

    @staticmethod
    def SetSpecificOnMatrix(matrix, list_of_tiles):
        """set tiles on matrix according to following list"""

        for tile in list_of_tiles:
            matrix[tile[0][0]][tile[0][1]] = tile[1]

    @staticmethod
    def BlitSpecificOnMap(surface, list_of_tiles):
        """blit tiles on map according to following list"""

        for tile in list_of_tiles:
            x_coord = SIZE_OF_TILE * tile[0][0]
            y_coord = SIZE_OF_TILE * tile[0][1]
            if tile[1] in [CHAR_FOR_PATH]:
                if (tile[0][0], tile[0][1]) in generated_floor:
                    surface.blit(generated_floor[(tile[0][0], tile[0][1])], (x_coord, y_coord))
                else:
                    generated_floor[(tile[0][0], tile[0][1])] = random.choice(list_with_floor)
                    surface.blit(generated_floor[(tile[0][0], tile[0][1])], (x_coord, y_coord))
            if tile[1] in [CHAR_FOR_CURRENT_POS]:
                pygame.draw.rect(surface, color=COLOR_FOR_CURRENT_POSITION,
                                 rect=[x_coord, y_coord, SIZE_OF_TILE, SIZE_OF_TILE])
            elif tile[1] in [CHAR_FOR_EXIT]:
                surface.blit(image_for_exit, (x_coord, y_coord))
            elif tile[1] in [CHAR_FOR_ANSWER]:
                pygame.draw.rect(surface, color=COLOR_FOR_ANSWER_TILES,
                                 rect=[x_coord, y_coord, SIZE_OF_TILE, SIZE_OF_TILE])
            else:
                surface.blit(image_for_empty, (x_coord, y_coord))

    def GetTile(self, position):
        """this function gives tile on the position of tile according to given x, y coordinates"""

        return self.matrix_with_map[position[0] // SIZE_OF_TILE][position[1] // SIZE_OF_TILE]

    @staticmethod
    def GetPositionOfTile(position):
        """this function gives position of tile according to given x, y coordinates"""

        return position[0] // SIZE_OF_TILE, position[1] // SIZE_OF_TILE

    def CanStandThere(self, position):
        """this function give info about possibility of standing on given position"""

        tile = self.GetTile((position[0] - self.global_map_position[0], position[1] - self.global_map_position[1]))
        return tile in [CHAR_FOR_PATH, CHAR_FOR_EXIT]

    def SetCurrentRoom(self, player_position, flag=False):
        """this function updates current map according to the given position"""

        if not flag:
            player_position = [player_position[0] - self.global_map_position[0],
                               player_position[1] - self.global_map_position[1]]
        if (self.GetPositionOfTile(player_position), self.GetTile(player_position)) not in self.tiles_for_current_room:
            current_room = []
            self.tiles_for_current_room = {}
            if self.GetTile(player_position) in [CHAR_FOR_PATH]:
                self.dfs.DFSOnTheSpecificTiles(self.GetPositionOfTile(player_position), self.matrix_with_map,
                                               current_room, [CHAR_FOR_PATH, CHAR_FOR_EXIT],
                                               depth=src.back.Config.LENGTH_OF_PATHS)
                self.tiles_for_current_room[
                    (self.GetPositionOfTile(player_position), self.GetTile(player_position))] = True
            elif self.GetTile(player_position) in [CHAR_FOR_EXIT]:
                src.front.Menus.MenuUI.ProcessingEndMenu()

            for tile in current_room:
                self.visited_tiles[tile] = True
            self.SetSpecificOnMatrix(self.matrix_with_visited, current_room)
            left_upper_corner = self.BlitSpecificMap(current_room)
            self.current_room_position = [
                self.global_map_position[0] + left_upper_corner[0] * SIZE_OF_TILE,
                self.global_map_position[1] + left_upper_corner[1] * SIZE_OF_TILE]
            current_room.append([self.GetPositionOfTile(player_position), CHAR_FOR_CURRENT_POS])
            self.BlitSpecificOnMap(self.visited_mappa, current_room)

    def Render(self, display):
        """this function blit map on the display"""

        display.blit(self.current_room, self.current_room_position)
        if src.back.Config.DIFFICULTY < 3:
            display.blit(pygame.transform.scale(self.visited_mappa, SIZE_OF_MINIMAP), POSITION_OF_MINIMAP)

    def MoveMap(self, vector_of_movement):
        """this function moves map according to movement vector"""

        self.global_map_position[0] += vector_of_movement[0]
        self.global_map_position[1] += vector_of_movement[1]
        self.current_room_position[0] += vector_of_movement[0]
        self.current_room_position[1] += vector_of_movement[1]

    def GetSpawnPositionOfPlayer(self):
        """this function generate spawn position of player"""
        x_coord_spawn = 0
        y_coord_spawn = 0
        sign = False
        for i in range(src.back.Config.SIZE_OF_MAP[0]):
            for j in range(src.back.Config.SIZE_OF_MAP[0]):
                if self.matrix_with_map[i][j] in [CHAR_FOR_PATH]:
                    x_coord_spawn = i
                    y_coord_spawn = j
                    sign = True
                    break
            if sign:
                break
        return x_coord_spawn, y_coord_spawn

    def GetSpawnPositionOfEnd(self):
        """this function generate spawn position of the end"""

        x_coord_end = 0
        y_coord_end = 0
        sign = False
        for i in range(src.back.Config.SIZE_OF_MAP[0])[::-1]:
            for j in range(src.back.Config.SIZE_OF_MAP[0])[::-1]:
                if self.matrix_with_map[i][j] in [CHAR_FOR_PATH]:
                    x_coord_end = i
                    y_coord_end = j
                    sign = True
                    break
            if sign:
                break
        return x_coord_end, y_coord_end

    def SpawnPosition(self):
        """this function sets spawn position and start map"""

        while True:
            spawn_pos_of_player = self.GetSpawnPositionOfPlayer()
            spawn_pos_of_end = self.GetSpawnPositionOfEnd()
            self.matrix_with_map[spawn_pos_of_end[0]][spawn_pos_of_end[1]] = CHAR_FOR_EXIT
            self.bfs.BFSForFindShortestPath((spawn_pos_of_player[0], spawn_pos_of_player[1]), self.matrix_with_map)
            self.answer = self.bfs.GetPath()

            self.global_map_position = [-spawn_pos_of_player[0] * SIZE_OF_TILE + SPAWN_POSITION[0],
                                        -spawn_pos_of_player[1] * SIZE_OF_TILE + SPAWN_POSITION[1]]
            self.SetCurrentRoom((spawn_pos_of_player[0] * SIZE_OF_TILE, spawn_pos_of_player[1] * SIZE_OF_TILE),
                                flag=True)
            return None

    def ShowAnswer(self):
        """this method puts answer on the mini-map"""

        src.back.Config.DIFFICULTY = 1
        self.BlitSpecificOnMap(self.visited_mappa, self.answer)
