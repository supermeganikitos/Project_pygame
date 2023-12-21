import pygame
import os
import sys

pygame.init()
size = width, height = 1550, 800
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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
        if self.rect.x > width:
            self.rect.x = self.image.get_size()[0] * -1
        self.rect = self.rect.move(self.vx, self.vy)


def draw_(screen, n):
    font = pygame.font.Font('Realest-Extended.otf', 85)
    text = font.render(str(n), True, pygame.Color('White'))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, pygame.Color('White'), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 10)


trucks = pygame.sprite.Group()
pygame.display.set_caption('simulator truck')
pygame.display.flip()
running = True
x_step = 150
y_step = 90
for x in range(0, width, x_step):
    for y in range(0, height, y_step):
        Truck(x, y, trucks)


clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    trucks.update()
    trucks.draw(screen)
    draw_(screen, 'Truck simulator')
    clock.tick(10)


    pygame.display.flip()