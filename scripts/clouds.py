import random


class Cloud:
    def __init__(self, pos, img, speed, depth) -> None:
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset=(0, 0)):
        render_pos = (
            self.pos[0] - offset[0] * self.depth,
            self.pos[1] - offset[1] * self.depth,
        )

        x_pixel = (
            render_pos[0] % (surf.get_width() + self.img.get_width())
            - self.img.get_width()
        )
        y_pixel = (
            render_pos[1] % (surf.get_height() + self.img.get_height())
            - self.img.get_height()
        )

        surf.blit(
            self.img,
            (
                x_pixel,
                y_pixel,
            ),
        )


class Clouds:
    def __init__(self, cloud_images, count=16) -> None:
        self.clouds = []

        # generate clouds
        for i in range(count):
            self.clouds.append(
                Cloud(
                    (
                        random.random() * 99999,
                        random.random() * 99999,
                    ),  # never mind the number it going to loop
                    random.choice(cloud_images),
                    random.random() * 0.05 + 0.55,  # speed
                    random.random() * 0.6 + 0.2,  # depth
                )
            )

        self.clouds.sort(key=lambda x: x.depth)  # will sort lower depth in the front

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)
