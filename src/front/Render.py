import pygame
from src.back.Config import *


def GetImage(path, size=SIZE_OF_TILE):
    result = pygame.image.load(path)
    result = pygame.transform.scale(result, (size, size))
    return result


def GetReversedSurfaceWithImage(image, size=SIZE_OF_TILE, flag='x'):
    surface = GetSurfaceWithImage(image, size)
    if flag == 'x':
        return pygame.transform.flip(surface, flip_x=True, flip_y=False)
    else:
        return pygame.transform.flip(surface, flip_x=False, flip_y=True)


def GetSurfaceWithImage(image, size=SIZE_OF_TILE):
    surface = pygame.Surface((size, size), flags=pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    surface.blit(image, (0, 0))
    return surface


dict_with_floors = {}

dict_with_chars = {}

dict_with_game_objects = {}


def SetSpritesForDeathAnimation():
    test = dict_with_game_objects
    for index in range(NUM_OF_SPRITES_FOR_DEATH_ANIMATION):
        dict_with_game_objects[SPRITE_ID_FOR_DEATH + str(index)] = GetSurfaceWithImage(
            GetImage(PATH_FOR_DEATH_ANIMATION + str(index).zfill(2) + FILE_WITH_IMAGES_EXTENSION, KNIGHT_SIZE),
            KNIGHT_SIZE)


def SetSpritesForGameObjects():
    test = dict_with_game_objects
    for index in range(NUM_OF_SPRITES_FOR_ATTACK):
        dict_with_game_objects[SPRITE_ID_FOR_ATTACK + RIGHT + str(index)] = GetSurfaceWithImage(
            GetImage(PATH_TO_SIDE_ATTACK + str(index) + FILE_WITH_IMAGES_EXTENSION, KNIGHT_SIZE), KNIGHT_SIZE)

        dict_with_game_objects[SPRITE_ID_FOR_ATTACK + LEFT + str(index)] = GetReversedSurfaceWithImage(
            GetImage(PATH_TO_SIDE_ATTACK + str(index) + FILE_WITH_IMAGES_EXTENSION, KNIGHT_SIZE), KNIGHT_SIZE)

        dict_with_game_objects[SPRITE_ID_FOR_ATTACK + UP + str(index)] = GetSurfaceWithImage(
            GetImage(PATH_TO_UPPER_ATTACK + str(index) + FILE_WITH_IMAGES_EXTENSION, KNIGHT_SIZE), KNIGHT_SIZE)

        dict_with_game_objects[SPRITE_ID_FOR_ATTACK + DOWN + str(index)] = GetReversedSurfaceWithImage(
            GetImage(PATH_TO_UPPER_ATTACK + str(index) + FILE_WITH_IMAGES_EXTENSION, KNIGHT_SIZE), KNIGHT_SIZE,
            flag='y')


def SetDictWithFloors():
    for index in range(1, NUM_OF_PNGS_FOR_FLOOR + 1):
        surface = pygame.Surface((SIZE_OF_TILE, SIZE_OF_TILE), flags=pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        surface.blit(GetImage(PATH_TO_FLOOR_PNG + str(index) + FILE_WITH_IMAGES_EXTENSION, SIZE_OF_TILE), (0, 0))
        dict_with_floors[index] = surface


def SetDictWithChars():
    surface = pygame.Surface((KNIGHT_SIZE, KNIGHT_SIZE), flags=pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    surface.blit(GetImage(PATH_TO_CHARACTER_PNG + 'Knight' + FILE_WITH_IMAGES_EXTENSION, KNIGHT_SIZE), (0, 0))
    dict_with_chars['Knight'] = surface


def GetFloorImage(floor_char):
    test = dict_with_floors
    return dict_with_floors[int(floor_char.split()[1])]


def SetImages():
    SetDictWithFloors()
    SetDictWithChars()
    SetSpritesForGameObjects()
    SetSpritesForDeathAnimation()
    test = 0


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
        self.game_objects = None
        self.mappa = mappa
        self.client = client

    def Update(self):
        self.players = self.client.GetPlayers()
        self.player = self.players[self.client.GetUser().GetUserId()]
        self.current_floors = self.mappa.GetCurrentRoomOfPlayer(self.player.GetStandHitBox())
        self.position_of_player_on_screen = (
            SPAWN_POSITION[0] - self.player.GetSize() / 2, SPAWN_POSITION[1] - self.player.GetSize() / 2)
        self.game_objects = self.client.GetGameObjects()

    def Draw(self):
        self.Update()
        self.display.fill(COLOR_FOR_BACKGROUND)
        self.DrawFloors()
        self.DrawPlayers()
        self.DrawGameObjects()
        self.DrawHealthBar()

    def DrawPlayers(self):
        self.DrawOtherPlayers()
        if not self.player.IsDead():
            self.DrawPlayer()

    def DrawCharacterAccordingToSide(self, player, position):
        character_image = dict_with_chars[self.player.GetName()]
        flipped_image = pygame.transform.flip(character_image, flip_x=True, flip_y=False)
        if player.GetSide() == LEFT:
            self.display.blit(flipped_image, (position[0], position[1]))
        else:
            self.display.blit(character_image, position)

    def DrawPlayer(self):
        self.display.blit(GetCharacterImageAccordingToSide(self.player.GetName(), self.player.GetSide()),
                          self.position_of_player_on_screen)

    def DrawOtherPlayers(self):
        for character in self.players.values():

            if character is not self.player and not character.IsDead() and self.mappa.IsPositionInListOfTiles(
                    character.GetStandHitBox(), self.current_floors):
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

    def DrawGameObjects(self):
        if self.game_objects is not None:
            for game_object in self.game_objects.values():
                if self.mappa.IsPositionInListOfTiles(game_object.GetPositionOfCenter(), self.current_floors):
                    self.display.blit(dict_with_game_objects[game_object.GetSpriteId()],
                                      (game_object.GetPosition()[0] - self.player.GetPosition()[0] +
                                       self.position_of_player_on_screen[0],
                                       game_object.GetPosition()[1] - self.player.GetPosition()[1] +
                                       self.position_of_player_on_screen[1]))

    def DrawHealthBar(self):
        health = self.player.GetHealth()
        pygame.draw.rect(self.display, COLOR_FOR_EMPTY_HEALTH_BAR, (
            POSITION_OF_HEALTH_BAR[0], POSITION_OF_HEALTH_BAR[1], self.player.GetMaxHealth() * PIXELS_PER_HEALTH_POINT,
            WIDTH_OF_HEALTH_BAR))
        pygame.draw.rect(self.display, COLOR_FOR_HEALTH_BAR, (
            POSITION_OF_HEALTH_BAR[0], POSITION_OF_HEALTH_BAR[1], health * PIXELS_PER_HEALTH_POINT,
            WIDTH_OF_HEALTH_BAR))
