import pygame




def draw(screen, n):
    screen.fill(pygame.Color('Black'))
    font = pygame.font.Font('Realest-Extended.otf', 85)
    text = font.render(str(n), True, pygame.Color('White'))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, pygame.Color('White'), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 10)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('simulator truck')
    size = width, height = 1550, 800
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw(screen, 'Truck simulator')
        pygame.display.flip()