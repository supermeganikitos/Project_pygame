import pygame
from trucks import Truck, trucks, SimpleButton

pygame.init()
size = width, height = 1550, 800
screen = pygame.display.set_mode(size)


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


pygame.display.set_caption('simulator truck')
listbtn = []
mimapbtn = SimpleButton(500, 500, 600, 100)
mimapbtn1 = SimpleButton(100, 100, 100, 100)
mimapbtn2 = SimpleButton(100, 100, 100, 100)
listbtn.append(mimapbtn)
listbtn.append(mimapbtn1)
listbtn.append(mimapbtn2)

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
    for i in listbtn:
        i.draw(screen)
    clock.tick(10)
    pygame.display.flip()