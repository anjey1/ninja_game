import os
import pygame

BASE_IMG_PATH = 'data/images/'


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0,0,0))
    return img

def load_images(path):
    images = []
    img_array = os.listdir(BASE_IMG_PATH + path)
    img_array.sort()
    for img_name in img_array:
        images.append(load_image(path + '/' + img_name))
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True) -> None:
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images,self.img_duration,self.loop)
    
    def update(self):
        # (0 + 1) % (5 * 5) - does the number matter hahahaha :))) = 1
        # (1 + 1) % (5 * 5) = 2
        if self.loop: 
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            # min(3+1, 5 * 2 - 1) - ?
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1) # idle ?
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
        
    def img(self):
        # WTF ?
        # 1 / 5 = 0.2
        # 2 / 5 = 0.4
        # 3 / 5 = 0.6
        # 4 / 5 = 0.8
        # 5 / 5 = 1
        return self.images[int(self.frame / self.img_duration)]