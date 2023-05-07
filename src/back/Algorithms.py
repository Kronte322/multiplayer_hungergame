"""File contains algorithms for generation"""

import random
import time
from abc import ABC, abstractmethod
from collections import deque

import src.back.Config as Config
import src.back.MapGenerator

random.seed(time.time())


class AlgoForGenerator(ABC):
    """this abstract class that represents algorithms for maze generation"""

    @abstractmethod
    def GetPathsForMap(self, vertex, matrix):
        """this function returns generated paths"""
        pass


class DFSAlgo(AlgoForGenerator):
    """this class represents deep first search algorithm"""

    def __init__(self):
        """initialize all that DFS algorithm requires"""

        self.used = {}
        self.parents = {}
        self.path = []

    def GetPath(self):
        """return passed during algorithm path"""

        return self.path

    def Clear(self):
        """clear variables of member class"""

        self.parents.clear()
        self.path.clear()
        self.used.clear()

    def CanBePlaced(self, vertex, matrix):
        """this function checks if can be placed path there"""

        sign = False
        for neighbour in sum(src.back.MapGenerator.MapGenerator.GetAround(vertex, matrix), []):
            if neighbour in [(-1, -1), vertex]:
                continue
            if neighbour == self.parents.get(vertex):
                continue
            if src.back.MapGenerator.MapGenerator.GetTile(neighbour, matrix) not in [Config.CHAR_FOR_EMPTY,
                                                                                     Config.CHAR_FOR_BOARD]:
                sign = True
                continue
            if self.used.get(neighbour):
                if neighbour in sum(
                        src.back.MapGenerator.MapGenerator.GetAroundForDFS(vertex, self.parents[vertex], matrix), []):
                    continue
                sign = True
                continue
        return not sign

    def GetPathsForMap(self, vertex, matrix):
        """this function returns generated paths"""

        self.DFSForPaths(vertex, matrix)
        return self.GetPath()

    def DFSForPaths(self, vertex, matrix):
        """random depth first search for generate random maze on empty matrix"""

        if not self.CanBePlaced(vertex, matrix):
            return
        self.used[vertex] = True
        self.path.append(vertex)
        neighbours = src.back.MapGenerator.MapGenerator.GetNeighbours(vertex, matrix).copy()
        while len(neighbours) != 0:
            row = random.choice(neighbours)
            neighbours.remove(row)
            if self.used.get(row) is None and row != self.parents.get(
                    vertex) and src.back.MapGenerator.MapGenerator.GetTile(row,
                                                                           matrix) not in [
                Config.CHAR_FOR_BOARD]:
                self.parents[row] = vertex
                self.DFSForPaths(row, matrix)

    def RecursiveCall(self, vertex, matrix, set_of_tiles, tiles, current_depth, depth):
        """help function for DFSOnTHeSpecificTiles"""

        self.used[vertex] = True
        self.path.append(vertex)
        set_of_tiles.append((vertex, src.back.MapGenerator.MapGenerator.GetTile(vertex, matrix)))
        if current_depth >= depth:
            return
        for neighbour in src.back.MapGenerator.MapGenerator.GetNeighbours(vertex, matrix):
            if src.back.MapGenerator.MapGenerator.GetTile(neighbour, matrix) in tiles:
                if self.used.get(neighbour) is None and neighbour != self.parents.get(vertex):
                    self.parents[neighbour] = vertex
                    self.RecursiveCall(neighbour, matrix, set_of_tiles, tiles, current_depth=current_depth + 1,
                                       depth=depth)

    def DFSOnTheSpecificTiles(self, vertex, matrix, set_of_tiles, tiles, depth=Config.DEFAULT_LENGTH_FOR_DFS):
        """DFs which goes across the following tiles"""

        self.Clear()
        self.RecursiveCall(vertex, matrix, set_of_tiles, tiles, current_depth=0, depth=depth)


class PrimaAlgo(AlgoForGenerator):
    """this class represents prima algorithm"""

    def __init__(self):
        """initialize all that requires prima algorithm"""

        self.opened = {}
        self.closed = {}
        self.parents = {}
        self.path = []

    def GetPath(self):
        """return passed during algorithm path"""

        return self.path

    def Clear(self):
        """clear variables of member class"""

        self.opened.clear()
        self.closed.clear()
        self.path.clear()

    def CanBePlaced(self, vertex, matrix):
        """this function checks if can be placed path there"""

        sign = False
        for neighbour in sum(src.back.MapGenerator.MapGenerator.GetAround(vertex, matrix), []):
            if neighbour in [(-1, -1), vertex]:
                continue
            if neighbour == self.parents.get(vertex):
                continue
            if src.back.MapGenerator.MapGenerator.GetTile(neighbour, matrix) not in [Config.CHAR_FOR_EMPTY,
                                                                                     Config.CHAR_FOR_BOARD]:
                sign = True
                continue
            if self.closed.get(neighbour):
                if neighbour in sum(
                        src.back.MapGenerator.MapGenerator.GetAroundForDFS(vertex, self.parents[vertex], matrix), []):
                    continue
                sign = True
                continue
        return not sign

    def GetPathsForMap(self, vertex, matrix):
        """this function returns generated paths"""

        self.PrimaForPaths(vertex, matrix)
        return self.GetPath()

    def PrimaForPaths(self, vertex, matrix):
        """prima algorithm with random choice from open tiles"""

        self.opened[vertex] = vertex

        while len(self.opened) != 0:
            if len(self.opened) == 1:
                current = list(self.opened.items())[0][0]
            else:
                current = random.choice(list(self.opened.values()))

            self.opened.pop(current)
            if not self.CanBePlaced(current, matrix):
                continue
            self.path.append(current)
            self.closed[current] = current

            for neighbour in src.back.MapGenerator.MapGenerator.GetNeighbours(current, matrix):
                if neighbour not in self.closed and src.back.MapGenerator.MapGenerator.GetTile(neighbour,
                                                                                               matrix) not in [
                    Config.CHAR_FOR_BOARD]:
                    self.opened[neighbour] = neighbour
                    self.parents[neighbour] = current


class BFSAlgo:
    """this class represents best first search algorithm"""

    def __init__(self):
        """initialize all that bfs algorithm requires"""

        self.deque = deque()
        self.closed = {}
        self.parents = {}
        self.dist = {}
        self.path = []

    def BFSForFindShortestPath(self, vertex, matrix):
        """this method perform a search the shortest path that complete maze using bfs algorithm"""

        self.deque.appendleft(vertex)
        current = vertex
        self.parents[current] = current

        while len(self.deque) != 0:
            current = self.deque.pop()
            self.closed[current] = True
            if src.back.MapGenerator.MapGenerator.GetTile(current, matrix) in [Config.CHAR_FOR_EXIT]:
                break

            for neighbour in src.back.MapGenerator.MapGenerator.GetNeighbours(current, matrix):
                if src.back.MapGenerator.MapGenerator.GetTile(neighbour, matrix) in [Config.CHAR_FOR_PATH,
                                                                                     Config.CHAR_FOR_EXIT]:
                    if neighbour not in self.closed:
                        self.parents[neighbour] = current
                        self.deque.appendleft(neighbour)

        while current != self.parents[current]:
            self.path.append([current, Config.CHAR_FOR_ANSWER])
            current = self.parents[current]
        self.path.append([current, Config.CHAR_FOR_ANSWER])

    def BFSOnTheSpecificTiles(self, vertex, matrix, list_with_visited, list_with_tiles, depth):
        self.deque.appendleft(vertex)
        current = vertex
        self.parents[current] = current
        self.dist[current] = 0
        while len(self.deque) != 0:
            current = self.deque.pop()
            self.closed[current] = True
            if self.dist[current] > depth:
                break
            list_with_visited.append((current, src.back.MapGenerator.MapGenerator.GetTile(current, matrix)))
            for neighbour in src.back.MapGenerator.MapGenerator.GetNeighbours(current, matrix):
                if src.back.MapGenerator.MapGenerator.GetTile(neighbour, matrix) in list_with_tiles:
                    if neighbour not in self.closed:
                        self.dist[neighbour] = self.dist[current] + 1
                        self.deque.appendleft(neighbour)

    def GetPath(self):
        """this method returns path that bfs algorithm has traveled"""

        return self.path

    def Clear(self):
        self.deque.clear()
        self.closed.clear()
        self.parents.clear()
        self.path.clear()
        self.dist.clear()
