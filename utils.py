import os
import pygame

BASE_IMG_PATH = "data/images/"
PIXELS_IN_TILE = 32
player_width = 40
player_height = 56


# Define a custom sprite class - Can be used for animations
class RectSprite(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = pygame.Surface((rect.width, rect.height))
        self.rect = rect

    def update(self):
        # Add any movement or update logic here
        # maybe we can use this somehow to update
        # the enemy rect inside enemy array without
        # returning the enemy object
        pass


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


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


def load_images_from_tile(path, flip=False):
    images = []
    img_array = os.listdir(BASE_IMG_PATH + path)
    img_array.sort()
    for img_name in img_array:
        images.append(load_image(path + "/" + img_name))

    images = [
        pygame.transform.scale(image, (player_width, player_height)) for image in images
    ]

    if flip:
        images = [pygame.transform.flip(image, True, False) for image in images]

    return images


def blit_all_tiles(game, window, tmxdata, world_offset):
    for layer in tmxdata:
        try:
            # layer['type'] != 'objectgroup': # and layer['name'] == 'Collision Layer':
            if hasattr(layer, "data"):  # dont paint shadow
                for index, tile in enumerate(layer.tiles()):
                    # tile[0] .... x grid location
                    # tile[1] .... y grid location
                    # tile[2] .... image data for blitting
                    tile = list(tile)
                    pixels_in_image = PIXELS_IN_TILE
                    x_pixel = (tile[0] * pixels_in_image) + world_offset[0]
                    y_pixel = (tile[1] * pixels_in_image) + world_offset[1]

                    # Animated Tiles
                    tile_props = tmxdata.get_tile_properties(tile[0], tile[1], 0)

                    # Add animated object
                    if (
                        tile_props != None
                        and tile_props.get("frames")
                        and (tile[0], tile[1]) not in game.animations
                    ):
                        from entities import Animate  # type: ignore

                        game.animations[(tile[0], tile[1])] = Animate(
                            tmxdata=tmxdata,
                            # Where to draw
                            x=x_pixel,
                            y=y_pixel,
                            # What to draw
                            tile_x=tile[0],
                            tile_y=tile[1],
                        )
                        # print(f"animation {tile[0]},{tile[1]}, added")
                    else:
                        # Static Tiles
                        tile_img = pygame.transform.scale(
                            tile[2], (PIXELS_IN_TILE, PIXELS_IN_TILE)
                        )

                        # draw the image according to world offset
                        window.blit(tile_img, (x_pixel, y_pixel))
            else:
                if layer.name == "Enemy":

                    # Add enemy object
                    if (layer.x, layer.y) not in game.enemies:
                        from entities import Enemy  # type: ignore

                        enemy = Enemy(
                            # Where to draw
                            x=layer.properties["tile_x"] * PIXELS_IN_TILE,
                            y=layer.properties["tile_y"] * PIXELS_IN_TILE,
                            # What to draw
                            tile_x=layer.properties["tile_x"],
                            tile_y=layer.properties["tile_y"],
                        )

                        # adding to enemies objects array for internal enemy logic
                        game.enemies[(layer.x, layer.y)] = enemy

                        # adding to enemies objects array for external enemy logic
                        enemy_rect = pygame.rect.Rect(
                            # Where to draw
                            layer.properties["tile_x"] * PIXELS_IN_TILE,
                            layer.properties["tile_y"] * PIXELS_IN_TILE,
                            # What to draw
                            enemy.width,
                            enemy.height,
                        )
                        enemy_sprite = RectSprite(enemy_rect)
                        game.enemies_group.append(enemy_sprite.rect)
                        enemy.group_index = len(game.enemies_group) - 1

        except:
            print("Error getting tiles on blit tiles from layer !")


def blit_all_enemies(game, window, tmxdata, world_offset):
    for layer in tmxdata:
        try:
            pass
            # layer['type'] != 'objectgroup': # and layer['name'] == 'Collision Layer':

        except:
            print("Error getting tiles on blit enemies from layer !")


def update_animations(game, window, world_offset):
    for tile in game.animations:
        game.animations[(tile[0], tile[1])].update(window, world_offset)


def update_enemies(game, tmxdata, window, world_offset):
    for tile in game.enemies:
        enemy = game.enemies[(tile[0], tile[1])].update(tmxdata, window, world_offset)
        game.enemies_group[enemy.group_index] = enemy.rect


def get_tile_properties(tmxdata, x, y, world_offset):
    world_x = x - world_offset[0]
    world_y = y - world_offset[1]
    tile_x = world_x // PIXELS_IN_TILE  # pixels in tile
    tile_y = world_y // PIXELS_IN_TILE  # pixels in tile

    # *********** Handle tile properties**************
    try:
        properties = tmxdata.get_tile_properties(tile_x, tile_y, 0)
    except ValueError:
        # Fill in missing tiles with default values and kill on sight
        properties = {
            "id": -1,
            "climable": 0,
            "ground": 0,
            "health": -9999,
            "points": 0,
            "provides": "",
            "requires": "",
            "solid": 0,
            "remove": False,
            "tile_x": tile_x,
            "tile_y": tile_y,
        }

    if properties is None:
        properties = {
            "id": -1,
            "climable": 0,
            "ground": 0,
            "health": 0,
            "points": 0,
            "provides": "",
            "requires": "",
            "solid": 0,
            "remove": False,
            "tile_x": tile_x,
            "tile_y": tile_y,
        }

    properties["x"] = tile_x
    properties["y"] = tile_y

    return properties


def get_tile_properties_enemy(tmxdata, x, y, world_offset):
    world_x = x
    world_y = y
    tile_x = world_x // PIXELS_IN_TILE  # pixels in tile
    tile_y = world_y // PIXELS_IN_TILE  # pixels in tile

    # *********** Handle tile properties**************
    try:

        properties = tmxdata.get_tile_properties(tile_x, tile_y, 0)
    except ValueError:
        # Fill in missing tiles with default values and kill on sight
        properties = {
            "id": -1,
            "climable": 0,
            "ground": 0,
            "health": -9999,
            "points": 0,
            "provides": "",
            "requires": "",
            "solid": 0,
            "remove": False,
            "tile_x": tile_x,
            "tile_y": tile_y,
        }

    if properties is None:
        properties = {
            "id": -1,
            "climable": 0,
            "ground": 0,
            "health": 0,
            "points": 0,
            "provides": "",
            "requires": "",
            "solid": 0,
            "remove": False,
            "tile_x": tile_x,
            "tile_y": tile_y,
        }

    properties["x"] = tile_x
    properties["y"] = tile_y

    return properties
