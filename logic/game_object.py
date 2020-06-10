from pygame.rect import Rect


class GameObject:
    def __init__(self, x, y, w, h, speed=(0, 0)):
        self.bounds = Rect(x, y, w, h)
        self.speed = speed

    @property
    def center(self):
        return self.bounds.center

    def move(self, dx, dy):
        self.bounds = self.bounds.move(dx, dy)

    def update(self):
        if self.speed == (0, 0):
            return
        self.move(*self.speed)
