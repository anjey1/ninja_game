import os
import pygame

BASE_IMG_PATH = "data/images/"
PIXELS_IN_TILE = 32
player_width = 50
player_height = 70


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


# the function that in charge of getting data from the tmx (Tiled App)
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
            "climable": 0,
            "ground": 0,
            "health": 0,
            "points": 0,
            "provides": "",
            "requires": "",
            "solid": 0,
        }

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
