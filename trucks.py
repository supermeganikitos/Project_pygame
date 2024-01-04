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


class SimpleButton(pygame.sprite.Sprite):
    def __init__(self, group, x, y, width, height, color=(100, 100, 100), text='', font_size=20):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font_size = font_size
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.font_size)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                            self.y + (self.height / 2 - text.get_height() / 2)))

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            print(1)
            return True

