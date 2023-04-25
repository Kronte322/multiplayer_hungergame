import pygame
from src.back.Config import *


def GetImage(path, size=SIZE_OF_TILE):
    result = pygame.image.load(path)
    result = pygame.transform.scale(result, (size, size))
    return result


dict_with_floors = {}

dict_with_chars = {}


def SetDictWithFloors():
    for index in range(1, NUM_OF_PNGS_FOR_FLOOR + 1):
        surface = pygame.Surface((SIZE_OF_TILE, SIZE_OF_TILE), flags=pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        surface.blit(GetImage(PATH_TO_FLOOR_PNG + str(index) + FILE_WITH_IMAGES_EXTENSION, SIZE_OF_TILE), (0, 0))
        dict_with_floors[index] = surface


def SetDictWithChars():
    surface = pygame.Surface((SIZE_OF_TILE, SIZE_OF_TILE), flags=pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    surface.blit(GetImage(PATH_TO_CHARACTER_PNG + 'Knight' + FILE_WITH_IMAGES_EXTENSION, KNIGHT_SIZE), (0, 0))
    dict_with_chars['Knight'] = surface


def GetFloorImage(floor_char):
    test = dict_with_floors
    return dict_with_floors[int(floor_char.split()[1])]


def SetImages():
    SetDictWithFloors()
    SetDictWithChars()


def GetCharacterImageAccordingToSide(character_name, side):
    character_image = dict_with_chars[character_name]
    if side == LEFT:
        return pygame.transform.flip(character_image, flip_x=True, flip_y=False)
    return character_image


class Render:
    SetImages()

    def __init__(self, display, mappa, client):
        self.display = display
        self.players = None
        self.player = None
        self.current_floors = None
        self.position_of_player_on_screen = None
        self.mappa = mappa
        self.client = client

    def Update(self):
        self.players = self.client.GetPlayers()
        self.player = self.players[self.client.GetUser().GetUserId()]
        self.current_floors = self.mappa.GetCurrentRoomOfPlayer(self.player.GetStandHitBox())
        self.position_of_player_on_screen = (
            SPAWN_POSITION[0] - self.player.GetSize() / 2, SPAWN_POSITION[1] - self.player.GetSize() / 2)

    def Draw(self):
        self.Update()
        self.display.fill(COLOR_FOR_BACKGROUND)
        self.DrawFloors()
        self.DrawPlayers()
        pygame.display.flip()

    def DrawPlayers(self):
        self.DrawPlayer()
        self.DrawOtherPlayers()

    def DrawPlayer(self):
        self.display.blit(GetCharacterImageAccordingToSide(self.player.GetName(), self.player.GetSide()),
                          self.position_of_player_on_screen)

    def DrawOtherPlayers(self):
        for character in self.players.values():
            if character is not self.player and self.mappa.IsPositionInListOfTiles(character.GetStandHitBox(),
                                                                                   self.current_floors):
                position_to_blit = (
                    character.GetPosition()[0] - self.player.GetPosition()[0] + self.position_of_player_on_screen[0],
                    character.GetPosition()[1] - self.player.GetPosition()[1] + self.position_of_player_on_screen[1])
                self.display.blit(GetCharacterImageAccordingToSide(character.GetName(), character.GetSide()),
                                  position_to_blit)

    def DrawFloors(self):
        for tile in self.current_floors:
            position_to_blit = (self.mappa.GetPositionOfTileInPixels(tile[0])[0] - self.player.GetPosition()[0] +
                                self.position_of_player_on_screen[0],
                                self.mappa.GetPositionOfTileInPixels(tile[0])[1] - self.player.GetPosition()[1] +
                                self.position_of_player_on_screen[1])
            self.display.blit(GetFloorImage(tile[1]), position_to_blit)
