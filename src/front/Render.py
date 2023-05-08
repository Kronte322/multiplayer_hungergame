"""File contains render"""

import pygame

import src.back.Config as Config


def GetImage(path, size=Config.SIZE_OF_TILE):
    """method returns resized image according to given path"""

    result = pygame.image.load(path)
    result = pygame.transform.scale(result, (size, size))
    return result


def GetReversedSurfaceWithImage(image, size=Config.SIZE_OF_TILE, flag='x'):
    """method returns reversed version of image"""

    surface = GetSurfaceWithImage(image, size)
    if flag == 'x':
        return pygame.transform.flip(surface, flip_x=True, flip_y=False)
    else:
        return pygame.transform.flip(surface, flip_x=False, flip_y=True)


def GetSurfaceWithImage(image, size=Config.SIZE_OF_TILE):
    """method returns surface with image"""

    surface = pygame.Surface((size, size), flags=pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    surface.blit(image, (0, 0))
    return surface


dict_with_floors = {}

dict_with_chars = {}

dict_with_game_objects = {}


def SetSpritesForDeathAnimation():
    """this method set sprites for death animation"""

    for index in range(Config.NUM_OF_SPRITES_FOR_DEATH_ANIMATION):
        dict_with_game_objects[Config.SPRITE_ID_FOR_DEATH + str(index)] = GetSurfaceWithImage(
            GetImage(Config.PATH_FOR_DEATH_ANIMATION + str(index).zfill(2) + Config.FILE_WITH_IMAGES_EXTENSION,
                     Config.KNIGHT_SIZE),
            Config.KNIGHT_SIZE)


def SetSpritesForGameObjects():
    """this method set sprites for game objects"""

    for index in range(Config.NUM_OF_SPRITES_FOR_ATTACK):
        dict_with_game_objects[Config.SPRITE_ID_FOR_ATTACK + Config.RIGHT + str(index)] = GetSurfaceWithImage(
            GetImage(Config.PATH_TO_SIDE_ATTACK + str(index) + Config.FILE_WITH_IMAGES_EXTENSION, Config.KNIGHT_SIZE),
            Config.KNIGHT_SIZE)

        dict_with_game_objects[Config.SPRITE_ID_FOR_ATTACK + Config.LEFT + str(index)] = GetReversedSurfaceWithImage(
            GetImage(Config.PATH_TO_SIDE_ATTACK + str(index) + Config.FILE_WITH_IMAGES_EXTENSION, Config.KNIGHT_SIZE),
            Config.KNIGHT_SIZE)

        dict_with_game_objects[Config.SPRITE_ID_FOR_ATTACK + Config.UP + str(index)] = GetSurfaceWithImage(
            GetImage(Config.PATH_TO_UPPER_ATTACK + str(index) + Config.FILE_WITH_IMAGES_EXTENSION, Config.KNIGHT_SIZE),
            Config.KNIGHT_SIZE)

        dict_with_game_objects[Config.SPRITE_ID_FOR_ATTACK + Config.DOWN + str(index)] = GetReversedSurfaceWithImage(
            GetImage(Config.PATH_TO_UPPER_ATTACK + str(index) + Config.FILE_WITH_IMAGES_EXTENSION, Config.KNIGHT_SIZE),
            Config.KNIGHT_SIZE,
            flag='y')


def SetDictWithFloors():
    """this method set sprites for floor"""

    for index in range(1, Config.NUM_OF_PNGS_FOR_FLOOR + 1):
        surface = pygame.Surface((Config.SIZE_OF_TILE, Config.SIZE_OF_TILE), flags=pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        surface.blit(
            GetImage(Config.PATH_TO_FLOOR_PNG + str(index) + Config.FILE_WITH_IMAGES_EXTENSION, Config.SIZE_OF_TILE),
            (0, 0))
        dict_with_floors[index] = surface


def SetDictWithChars():
    """this method set sprites with characters"""

    surface = pygame.Surface((Config.KNIGHT_SIZE, Config.KNIGHT_SIZE), flags=pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    surface.blit(
        GetImage(Config.PATH_TO_CHARACTER_PNG + 'Knight' + Config.FILE_WITH_IMAGES_EXTENSION, Config.KNIGHT_SIZE),
        (0, 0))
    dict_with_chars['Knight'] = surface


def GetFloorImage(floor_char):
    """this method returns surface according to given id"""

    return dict_with_floors[int(floor_char.split()[1])]


def SetImages():
    """this method sets images"""

    SetDictWithFloors()
    SetDictWithChars()
    SetSpritesForGameObjects()
    SetSpritesForDeathAnimation()


def GetCharacterImageAccordingToSide(character_name, side):
    """this method return char image according to side"""

    character_image = dict_with_chars[character_name]
    if side == Config.LEFT:
        return pygame.transform.flip(character_image, flip_x=True, flip_y=False)
    return character_image


class Render:
    """this class represents work with user display"""

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
        """this method update game objects"""

        self.players = self.client.GetPlayers()
        self.player = self.players[self.client.GetUser().GetUserId()]
        self.current_floors = self.mappa.GetCurrentRoomOfPlayer(self.player.GetStandHitBox())
        self.position_of_player_on_screen = (
            Config.SPAWN_POSITION[0] - self.player.GetSize() / 2, Config.SPAWN_POSITION[1] - self.player.GetSize() / 2)
        self.game_objects = self.client.GetGameObjects()

    def Draw(self):
        """this method draw all stuff on the screen"""

        self.Update()
        self.display.fill(Config.COLOR_FOR_BACKGROUND)
        self.DrawFloors()
        self.DrawPlayers()
        self.DrawGameObjects()
        self.DrawHealthBar()

    def DrawPlayers(self):
        """this method draws players"""

        self.DrawOtherPlayers()
        if not self.player.IsDead():
            self.DrawPlayer()

    def DrawPlayer(self):
        """this method draws users player"""

        self.display.blit(GetCharacterImageAccordingToSide(self.player.GetName(), self.player.GetSide()),
                          self.position_of_player_on_screen)

    def DrawOtherPlayers(self):
        """this method draws other players"""

        for character in self.players.values():

            if character is not self.player and not character.IsDead() and self.mappa.IsPositionInListOfTiles(
                    character.GetStandHitBox(), self.current_floors):
                position_to_blit = (
                    character.GetPosition()[0] - self.player.GetPosition()[0] + self.position_of_player_on_screen[0],
                    character.GetPosition()[1] - self.player.GetPosition()[1] + self.position_of_player_on_screen[1])
                self.display.blit(GetCharacterImageAccordingToSide(character.GetName(), character.GetSide()),
                                  position_to_blit)

    def DrawFloors(self):
        """this method draws floor"""

        for tile in self.current_floors:
            position_to_blit = (self.mappa.GetPositionOfTileInPixels(tile[0])[0] - self.player.GetPosition()[0] +
                                self.position_of_player_on_screen[0],
                                self.mappa.GetPositionOfTileInPixels(tile[0])[1] - self.player.GetPosition()[1] +
                                self.position_of_player_on_screen[1])
            self.display.blit(GetFloorImage(tile[1]), position_to_blit)

    def DrawGameObjects(self):
        """this method draws game objects"""

        if self.game_objects is not None:
            for game_object in self.game_objects.values():
                if self.mappa.IsPositionInListOfTiles(game_object.GetPositionOfCenter(), self.current_floors):
                    self.display.blit(dict_with_game_objects[game_object.GetSpriteId()],
                                      (game_object.GetPosition()[0] - self.player.GetPosition()[0] +
                                       self.position_of_player_on_screen[0],
                                       game_object.GetPosition()[1] - self.player.GetPosition()[1] +
                                       self.position_of_player_on_screen[1]))

    def DrawHealthBar(self):
        """this method draw health bar"""

        health = self.player.GetHealth()
        pygame.draw.rect(self.display, Config.COLOR_FOR_EMPTY_HEALTH_BAR, (
            Config.POSITION_OF_HEALTH_BAR[0], Config.POSITION_OF_HEALTH_BAR[1],
            self.player.GetMaxHealth() * Config.PIXELS_PER_HEALTH_POINT,
            Config.WIDTH_OF_HEALTH_BAR))
        pygame.draw.rect(self.display, Config.COLOR_FOR_HEALTH_BAR, (
            Config.POSITION_OF_HEALTH_BAR[0], Config.POSITION_OF_HEALTH_BAR[1], health * Config.PIXELS_PER_HEALTH_POINT,
            Config.WIDTH_OF_HEALTH_BAR))
