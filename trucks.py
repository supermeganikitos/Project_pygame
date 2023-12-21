import pygame
import os
import sys

trucks = pygame.sprite.Group()
pygame.init()
size = width, height = 1550, 800
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Truck(pygame.sprite.Sprite):
    image = load_image("truck.png", -1)

    def __init__(self, x, y, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Truck.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.vx = 1
        self.vy = 0
        self.add(trucks)

    def update(self):
        if self.rect.x > 1550:
            self.rect.x = self.image.get_size()[0] * -1
        self.rect = self.rect.move(self.vx, self.vy)


class SimpleButton(pygame.sprite.Sprite):  # от него будем наследовать все кнопки и destination тоже
    def __init__(self, group, x, y, size_x=10, size_y=10, color=(200, 200, 200)):
        super().__init__(*group)
        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)

        pygame.draw.rect(self.image, pygame.Color(color),
                         (0, 0, size_x, size_y))
        self.rect = pygame.Rect(x, y, size_x, size_y)


class MaskButton(SimpleButton):  # от него будем наследовать все кнопки и destination тоже
    def __init__(self, group, x, y, img_name):
        super().__init__(group, x, y, size_x=10, size_y=10, color=(0, 0, 0))
        self.image = load_image(img_name)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Truck1:
    def __init__(self):
        pass

    def func(self):
        pass






