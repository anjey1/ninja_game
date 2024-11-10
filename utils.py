import os
import pygame

BASE_IMG_PATH = "data/images/"
PIXELS_IN_TILE = 32
player_width = 50
player_height = 70

# LOADING


# the function in charge of loading images/sprites
def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


# this function is in charge of loading sets of images into array
def load_images(path, flip=False, img_width=player_width, img_height=player_height):
    images = []
    img_array = os.listdir(BASE_IMG_PATH + path)
    img_array.sort()
    for img_name in img_array:
        images.append(load_image(path + "/" + img_name))

    images = [
        pygame.transform.scale(image, (img_width, img_height)) for image in images
    ]

    if flip:
        images = [pygame.transform.flip(image, True, False) for image in images]

    return images


# DRAWING


# the function that in charge of painting data from the tmx (Tiled App)
def blit_all_tiles(window, tmxdata, world_offset):
    for layer in tmxdata:
        try:
            # layer['type'] != 'objectgroup': # and layer['name'] == 'Collision Layer':
            if layer.id in [1, 2]:
                for tile in layer.tiles():
                    # tile[0] .... x grid location
                    # tile[1] .... y grid location
                    # tile[2] .... image data for blitting
                    pixels_in_image = 32
                    img = pygame.transform.scale(tile[2], (32, 32))
                    x_pixel = tile[0] * pixels_in_image + world_offset[0]
                    y_pixel = tile[1] * pixels_in_image + world_offset[1]
                    # draw the image according to world offset
                    window.blit(img, (x_pixel, y_pixel))
            # else:
            #     for obj in layer:
            #         col_rect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
            #     collision_rects.append(col_rect)
        except:
            print("Warning !")
            print(layer.tiles())


def drawInticator(
    window,
    x=0,
    y=0,
    color=(255, 255, 0),
    indicatorSize=16,
):
    """_summary_

    Args:
        window (_type_): _description_
        x (int, optional): _description_. Defaults to 0.
        y (int, optional): _description_. Defaults to 0.
        color (tuple, optional): _description_. Defaults to (255, 255, 0).
        indicatorSize (int, optional): _description_. Defaults to 16.
    """

    pygame.draw.rect(
        window,
        (color),
        (
            # Where
            x,
            y,
            # What Size
            indicatorSize,
            indicatorSize,
        ),
        2,
    )


# Sampeling Map - Get Props of tile


# the function that in charge of getting data from the tmx (Tiled App)
def get_tile_properties(tmxdata, x, y, world_offset):
    """Get tile properties for player instances\n
        Remmember the great tale about the world offset\n
        He who shifts the screen

    Args:
        tmxdata (tmxdata): tmx map json of numbers
        x (int): x player location
        y (int): y player location
        world_offset (int[]): world_offset [x=50,y=30]

    Returns:
        dict: {"climable": 0,"ground": 0,"health": 0,"points": 0,"provides": "","requires": "","solid": 0}
    """
    world_x = x - world_offset[0]
    world_y = y - world_offset[1]
    tile_x = world_x // PIXELS_IN_TILE  # pixels in tile
    tile_y = world_y // PIXELS_IN_TILE  # pixels in tile

    # *********** Handle tile properties**************
    try:
        properties = tmxdata.get_tile_properties(tile_x, tile_y, 0)
    except ValueError:
        # Return when touching Sprite out of map
        properties = {
            "climable": 0,
            "ground": 0,
            "health": 0,
            "points": 0,
            "provides": "",
            "requires": "",
            "solid": 0,
        }
    except TypeError:
        pass

    # Return when touching Empty Sprite
    if properties is None:
        properties = {
            "climable": 0,
            "ground": 0,
            "health": 0,
            "points": 0,
            "provides": "",
            "requires": "",
            "solid": 0,
        }
    return properties


# the function that in charge of getting data from the tmx (Tiled App)
def get_tile_properties_enemies(tmxdata, x, y, world_offset):
    """Get tile properties for enemies instances\n
    Remmember the great tale about the world offset\n
    He who shifts the screen

    Args:
        tmxdata (tmxdata): tmx map json of numbers
        x (int): x enemy location
        y (int): y enemy location
        world_offset (int[]): world_offset [x=50,y=30]

    Returns:
        dict: {"climable": 0,"ground": 0,"health": 0,"points": 0,"provides": "","requires": "","solid": 0}
    """
    world_x = x
    world_y = y
    tile_x = world_x // PIXELS_IN_TILE  # pixels in tile
    tile_y = world_y // PIXELS_IN_TILE  # pixels in tile

    # *********** Handle tile properties**************
    try:
        properties = tmxdata.get_tile_properties(tile_x, tile_y, 0)
    except ValueError:
        # Return when touching Sprite out of map
        properties = {
            "climable": 0,
            "ground": 0,
            "health": 0,
            "points": 0,
            "provides": "",
            "requires": "",
            "solid": 0,
        }

    # Return when touching Empty Sprite
    if properties is None:
        properties = {
            "climable": 0,
            "ground": 0,
            "health": 0,
            "points": 0,
            "provides": "",
            "requires": "",
            "solid": 0,
        }
    return properties


def update_enemies(game, tmxdata, window, world_offset):
    for enemy in game.enemies_group:
        enemy.update(tmxdata, window)
        enemy.render(window, world_offset)


def moveWindow(game, window, player):
    # World Moves - Handle world offset
    # print(f"{self.player.y,self.player.x}")
    if player.y < 134:
        player.y = 134
        game.world_offset[1] += 10

    if player.y > game.y:
        player.y = game.y
        game.world_offset[1] -= 10

    if player.x < 340:
        player.x = 340
        game.world_offset[0] += 10

    if player.x > window.get_width() - 340 - 50:
        player.x = window.get_width() - 340 - 50
        game.world_offset[0] -= 10
