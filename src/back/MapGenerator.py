"""File contains map generator"""

import random

import src.back.Config as Config


class MapGenerator:
    """this class make able to generate maze and make able to operate with it"""

    @staticmethod
    def GenerateMaze(size, algorithm, seed):
        """generate maze as matrix with following size"""
        random.seed(seed)
        maze = []
        MapGenerator.CreateMatrix(maze, size)
        MapGenerator.SetBoardsOfMap(maze)
        MapGenerator.SetPathsOnMap(maze, algorithm)
        MapGenerator.SetRandomFloorsOnMap(maze)
        return maze

    @staticmethod
    def SetRandomFloorsOnMap(matrix):
        for i in range(Config.NUM_OF_RANDOM_TILES):
            x_coord = random.randint(1, len(matrix) - 2)
            y_coord = random.randint(1, len(matrix[0]) - 2)
            matrix[x_coord][y_coord] = Config.CHAR_FOR_PATH

    @staticmethod
    def GetClearMap(size):
        """generate empty matrix with following size"""

        result = []
        MapGenerator.CreateMatrix(result, size)
        return result

    @staticmethod
    def GetTile(position: tuple, matrix):
        """return what tile on following position in matrix"""

        return matrix[int(position[0])][int(position[1])]

    @staticmethod
    def GetNeighbours(position: tuple, matrix):
        """return nearby tiles by cross on following position in matrix"""

        result = []
        if position[0] > 0:
            result.append((position[0] - 1, position[1]))
        if position[0] < len(matrix) - 1:
            result.append((position[0] + 1, position[1]))
        if position[1] > 0:
            result.append((position[0], position[1] - 1))
        if position[1] < len(matrix[0]) - 1:
            result.append((position[0], position[1] + 1))
        return result

    @staticmethod
    def GetAround(position: tuple, matrix):
        """return all nearby tiles on following position in matrix"""

        # просто ифаю девять случаев не вижу нужды разбивать это на три функции

        result = []
        intermediate = []

        if position[0] > 0 and position[1] > 0:
            intermediate.append((position[0] - 1, position[1] - 1))
        else:
            intermediate.append((-1, -1))
        if position[0] > 0:
            intermediate.append((position[0] - 1, position[1]))
        else:
            intermediate.append((-1, -1))
        if position[0] > 0 and position[1] < len(matrix[0]) - 1:
            intermediate.append((position[0] - 1, position[1] + 1))
        else:
            intermediate.append((-1, -1))
        result.append(intermediate.copy())

        intermediate.clear()

        if position[1] > 0:
            intermediate.append((position[0], position[1] - 1))
        else:
            intermediate.append((-1, -1))
        intermediate.append((position[0], position[1]))
        if position[1] < len(matrix[0]) - 1:
            intermediate.append((position[0], position[1] + 1))
        else:
            intermediate.append((-1, -1))
        result.append(intermediate.copy())

        intermediate.clear()

        if position[0] < len(matrix) - 1 and position[1] > 0:
            intermediate.append((position[0] + 1, position[1] - 1))
        else:
            intermediate.append((-1, -1))
        if position[0] < len(matrix) - 1:
            intermediate.append((position[0] + 1, position[1]))
        else:
            intermediate.append((-1, -1))
        if position[0] < len(matrix) - 1 and position[1] < len(matrix[0]) - 1:
            intermediate.append((position[0] + 1, position[1] + 1))
        else:
            intermediate.append((-1, -1))
        result.append(intermediate.copy())

        intermediate.clear()

        return result

    @staticmethod
    def GetLeftAround(position, matrix):
        """return all nearby tiles on following position without right column"""

        around = MapGenerator.GetAround(position, matrix).copy()
        around.pop()
        return around

    @staticmethod
    def GetUpAround(position, matrix):
        """return all nearby tiles on following position bottom row"""

        around = MapGenerator.GetAround(position, matrix)
        res = []
        for tile in range(len(around)):
            intermediate = []
            for j in range(len(around[0]) - 1):
                intermediate.append(around[tile][j])
            res.append(intermediate)
        return res

    @staticmethod
    def GetRightAround(position, matrix):
        """return all nearby tiles on following position without left column"""

        around = MapGenerator.GetAround(position, matrix)
        res = []
        for tile in range(1, len(around)):
            res.append(around[tile])
        return res

    @staticmethod
    def GetDownAround(position, matrix):
        """return all nearby tiles on following position without top row"""

        around = MapGenerator.GetAround(position, matrix)
        res = []
        for i in range(len(around)):
            intermediate = []
            for j in range(1, len(around[0])):
                intermediate.append(around[i][j])
            res.append(intermediate)
        return res

    @staticmethod
    def GetAroundForDFS(position, parent, matrix):
        """return nearby tiles on following position for dfs algorithm according to parent of the tile"""

        if position[0] > parent[0]:
            return MapGenerator.GetLeftAround(parent, matrix)
        if position[0] < parent[0]:
            return MapGenerator.GetRightAround(parent, matrix)
        if position[1] > parent[1]:
            return MapGenerator.GetUpAround(parent, matrix)
        if position[1] < parent[1]:
            return MapGenerator.GetDownAround(parent, matrix)

    @staticmethod
    def CreateMatrix(matrix, size):
        """create matrix with specific size"""

        for i in range(size[0]):
            intermediate = []
            for j in range(size[1]):
                intermediate.append(Config.CHAR_FOR_EMPTY)
            matrix.append(intermediate)

    @staticmethod
    def SetBoardsOfMap(matrix):
        """set boards on matrix like picture frame, for avoiding some troubles with boarders"""

        for i in range(len(matrix)):
            matrix[i][0] = Config.CHAR_FOR_BOARD
        for i in range(len(matrix[0])):
            matrix[len(matrix) - 1][i] = Config.CHAR_FOR_BOARD
        for i in range(len(matrix)):
            matrix[i][len(matrix[0]) - 1] = Config.CHAR_FOR_BOARD
        for i in range(len(matrix[0])):
            matrix[0][i] = Config.CHAR_FOR_BOARD

    @staticmethod
    def SetPathsOnMap(matrix, algorithm):
        """set paths on map using specific algorithm"""

        first_coord = random.randrange(1, Config.SIZE_OF_MAP[0] - 1)
        second_coord = random.randrange(1, Config.SIZE_OF_MAP[1] - 1)
        for tile in algorithm.GetPathsForMap((first_coord, second_coord), matrix):
            matrix[tile[0]][tile[1]] = Config.CHAR_FOR_PATH

    @staticmethod
    def ClearMatrix(matrix):
        """fill matrix with empty tile"""

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = Config.CHAR_FOR_EMPTY
