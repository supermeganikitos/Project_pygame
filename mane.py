import pygame
from trucks import Truck, trucks, SimpleButton

SHOW_MINIMAP = 1
SHOW_PREWIEW = 2
SHOW_ROAD = 3

pygame.init()


def draw_(screen, n, width, height, textsize=85, delta_frame=None,
          width_frame=None, text_color='White', frame_color='White', font='Realest-Extended.otf'):
    font = pygame.font.Font(font, textsize)
    text = font.render(str(n), True, pygame.Color(text_color))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    if delta_frame and width_frame:
        pygame.draw.rect(screen, pygame.Color(frame_color),
                         (text_x - delta_frame, text_y - delta_frame,
                          text_w + delta_frame * 2, text_h + delta_frame * 2), width_frame)


def running_preview():
    size = width, height = 1550, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('simulator truck')
    group_preview = pygame.sprite.Group()
    mimapbtn = SimpleButton(group_preview, 500, 500, 600, 100, pygame.Color('white'), text='minimap')
    pygame.display.flip()
    x_step = 150
    y_step = 90
    for x in range(0, width, x_step):
        for y in range(0, height, y_step):
            Truck(x, y, trucks)
    clock = pygame.time.Clock()
    runningpreview = True
    res = False
    flag = False
    while runningpreview:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningpreview = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                res = mimapbtn.update(event)
                if res:
                    flag = True
                    break
        if flag:
            break
        trucks.update()
        trucks.draw(screen)
        draw_(screen, 'Truck simulator', width, height, delta_frame=10, width_frame=10)
        mimapbtn.draw(screen)
        clock.tick(10)
        pygame.display.flip()
    if res:
        return SHOW_MINIMAP


def running_minimap():
    size = width, height = 550, 690
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('simulator truck')
    bg = pygame.image.load("Roads.png")
    screen.blit(bg, (0, 0))
    clock = pygame.time.Clock()
    runningminimap = True
    while runningminimap:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningminimap = False
        clock.tick(10)
        pygame.display.flip()


run_preview = running_preview()
if run_preview == SHOW_MINIMAP:
    running_minimap()