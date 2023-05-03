"""File contains map class"""

import pygame
from src.back.MapGenerator import *
from src.back.Config import *
import src.back.Config
import src.back.Algorithms as Algo
import src.front.Menus


class Map:
    def __init__(self, seed, size_of_map=SIZE_OF_MAP, size_of_tile_of_map=SIZE_OF_TILE):
        """initialize map"""

        self.size_of_map = size_of_map
        self.size_of_tile = size_of_tile_of_map
        self.matrix_with_map = MapGenerator.GenerateMaze(size_of_map, Algo.DFSAlgo(), seed)
        self.SetFloors()
        self.bfs = BFSAlgo()
        self.current_rooms = {}

    def SetFloors(self):
        for x_coord in range(self.size_of_map[0]):
            for y_coord in range(self.size_of_map[1]):
                if self.GetTile((x_coord, y_coord)) in [CHAR_FOR_FLOOR]:
                    self.SetSpecificOnMap([((x_coord, y_coord), random.choice(CHARS_FOR_FLOORS))])

    def GetPositionOfTileInPixels(self, position_of_tile):
        return position_of_tile[0] * self.size_of_tile, position_of_tile[1] * self.size_of_tile

    def SetSpecificOnMap(self, list_of_tiles):
        """set tiles on matrix according to following list"""

        for tile in list_of_tiles:
            self.matrix_with_map[tile[0][0]][tile[0][1]] = tile[1]

    def GetTile(self, position, position_in_pixels=False):
        """this function gives tile on the position of tile according to given x, y coordinates"""
        if position_in_pixels:
            return self.matrix_with_map[int(position[0] // self.size_of_tile)][int(position[1] // self.size_of_tile)]
        return self.matrix_with_map[position[0]][position[1]]

    def GetPositionOfTile(self, position):
        """this function gives position of tile according to given x, y coordinates"""

        return position[0] // self.size_of_tile, position[1] // self.size_of_tile

    def CanStandThere(self, position):
        """this function give info about possibility of standing on given position"""

        tile = self.GetTile(position, position_in_pixels=True)
        return tile in [CHAR_FOR_PATH] + CHARS_FOR_FLOORS

    def IsPositionInListOfTiles(self, position, list_of_tiles):
        return self.GetPositionOfTile(position) in [tile[0] for tile in list_of_tiles]

    def SetCurrentRooms(self):
        for x_coord in range(self.size_of_map[0]):
            for y_coord in range(self.size_of_map[1]):
                current_room = []
                if self.GetTile((x_coord, y_coord)) in CHARS_FOR_FLOORS + [CHAR_FOR_FLOOR]:
                    self.bfs.Clear()
                    self.bfs.BFSOnTheSpecificTiles((x_coord, y_coord), self.matrix_with_map,
                                                   current_room, [CHAR_FOR_PATH, CHAR_FOR_EXIT] + CHARS_FOR_FLOORS,
                                                   depth=src.back.Config.LENGTH_OF_PATHS)
                    self.current_rooms[(x_coord, y_coord)] = current_room

    def GetCurrentRoomOfPlayer(self, player_position):
        """this function updates current map according to the given position"""

        current_room = []
        if self.GetTile(player_position, position_in_pixels=True) in [CHAR_FOR_PATH] + CHARS_FOR_FLOORS:
            if self.GetPositionOfTile(player_position) in self.current_rooms:
                return self.current_rooms[self.GetPositionOfTile(player_position)]
            self.bfs.Clear()
            self.bfs.BFSOnTheSpecificTiles(self.GetPositionOfTile(player_position), self.matrix_with_map,
                                           current_room, [CHAR_FOR_PATH, CHAR_FOR_EXIT] + CHARS_FOR_FLOORS,
                                           depth=src.back.Config.LENGTH_OF_PATHS)
            self.current_rooms[self.GetPositionOfTile(player_position)] = current_room
        return current_room

    def GetSpawnPositionOfPlayer(self):
        """this function generate spawn position of player"""

        random.seed(time.time())
        while True:
            x_coord_spawn = random.randint(0, self.size_of_map[0] - 1)
            y_coord_spawn = random.randint(0, self.size_of_map[1] - 1)
            if self.GetTile((x_coord_spawn, y_coord_spawn)) in [CHAR_FOR_PATH] + CHARS_FOR_FLOORS:
                return [x_coord_spawn * self.size_of_tile, y_coord_spawn * self.size_of_tile]
