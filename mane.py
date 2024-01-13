import pygame
import sys
import os
from trucks import Truck, trucks, SimpleButton, load_image

SHOW_MINIMAP = 1
SHOW_PREWIEW = 2
SHOW_ROAD = 3
EXIT_FROM_GAME = 4
BACK_TO_MENU = 5
run_the_first_time = True

pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


def draw_(screen, n, width, height, textsize=85, delta_frame=None,
          width_frame=None, text_color='White', frame_color='White', font='Realest-Extended.otf'):
    font = pygame.font.Font(font, textsize)
    text = font.render(str(n), True, pygame.Color(text_color))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 4 - text.get_height() // 2
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
    pygame.mixer.music.load('data/autro.mp3')
    pygame.mixer.music.play(-1)

    play = SimpleButton(group_preview, 500, 290, 600, 100, pygame.Color('white'), text='play new')
    save = SimpleButton(group_preview, 500, 400, 600, 100, pygame.Color('white'), text='return to last save')
    mimapbtn = SimpleButton(group_preview, 500, 510, 600, 100, pygame.Color('white'), text='minimap')
    quitq = SimpleButton(group_preview, 500, 620, 600, 100, pygame.Color('white'), text='quit')
    pygame.display.flip()
    x_step = 150
    y_step = 90
    if run_the_first_time:
        for x in range(0, width, x_step):
            for y in range(0, height, y_step):
                Truck(x, y, trucks)
    clock = pygame.time.Clock()
    runningpreview = True
    res = False
    res1 = False
    flag = False
    while runningpreview:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                res = mimapbtn.update(event)
                res1 = quitq.update(event)
                if res or res1:
                    flag = True
                    break
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    pygame.mixer.music.pause()
                elif event.key == pygame.K_2:
                    pygame.mixer.music.unpause()
        if flag:
            break
        trucks.update()
        trucks.draw(screen)
        draw_(screen, 'Truck simulator', width, height, delta_frame=10, width_frame=10)
        play.draw(screen)
        save.draw(screen)
        mimapbtn.draw(screen)
        quitq.draw(screen)
        clock.tick(10)
        pygame.display.flip()
    if res:
        return SHOW_MINIMAP
    if res1:
        return EXIT_FROM_GAME


def running_minimap():
    size = width, height = 550, 690
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('simulator truck')
    bg = pygame.image.load("Roads.png")
    screen.blit(bg, (0, 0))
    clock = pygame.time.Clock()
    runningminimap = True
    dest = pygame.sprite.Group()
    quit_to_the_menu = SimpleButton(dest, 450, 0, 100, 50, pygame.Color('yellow'), text='В меню', font_size=10)
    moscow = SimpleButton(dest, 430, 100, 40, 25, pygame.Color('yellow'), text='Moscow', font_size=10)
    kazan = SimpleButton(dest, 70, 50, 40, 25, pygame.Color('yellow'), text='Kazan', font_size=10)
    saratov = SimpleButton(dest, 170, 170, 40, 25, pygame.Color('yellow'), text='Saratov', font_size=10)
    samara = SimpleButton(dest, 60, 405, 40, 25, pygame.Color('yellow'), text='Samara', font_size=10)
    tyla = SimpleButton(dest, 50, 555, 40, 25, pygame.Color('yellow'), text='Tyla', font_size=10)
    penza = SimpleButton(dest, 380, 445, 40, 25, pygame.Color('yellow'), text='Penza', font_size=10)
    piter = SimpleButton(dest, 500, 425, 40, 25, pygame.Color('yellow'), text='Piter', font_size=10)
    dests = {1: moscow, 2: kazan, 3: saratov, 4: samara, 5: tyla, 6: penza, 7: piter}
    current_destination = (
        input('Выберите начальную точку: moscow: 1, kazan: 2, saratov: 3, samara: 4, tyla: 5, penza: 6, piter: 7'))
    while current_destination not in '1234567':
        current_destination = (
            input('Выберите начальную точку: moscow: 1, kazan: 2, saratov: 3, samara: 4, tyla: 5, penza: 6, piter: 7'))
    current_destination = dests[int(current_destination)]
    connected_destinations = {moscow: (piter, penza, samara, kazan),
                              kazan: (saratov, moscow),
                              saratov: (kazan, samara),
                              samara: (saratov, moscow, tyla),
                              tyla: (penza, samara, piter),
                              penza: (piter, moscow, tyla),
                              piter: (moscow, tyla, penza)}
    roads_files = {(moscow, kazan): '1-2.txt', (moscow, kazan)[::-1]: '1-2.txt',
                   (moscow, samara): '1-5.txt', (moscow, samara)[::-1]: '1-5.txt',
                   (moscow, penza): '1-6.txt', (moscow, penza)[::-1]: '1-6.txt',
                   (moscow, piter): '1-7.txt', (moscow, piter)[::-1]: '1-7.txt',
                   (saratov, kazan): '3-2.txt', (saratov, kazan)[::-1]: '3-2.txt',
                   (samara, saratov): '4-3.txt', (samara, saratov)[::-1]: '4-3.txt',
                   (samara, tyla): '4-5.txt', (samara, tyla)[::-1]: '4-5.txt',
                   (penza, tyla): '6-5.txt', (penza, tyla)[::-1]: '6-5.txt',
                   (penza, piter): '6-7.txt', (penza, piter)[::-1]: '6-7.txt',
                   (tyla, piter): '5-7.txt', (tyla, piter)[::-1]: '5-7.txt'}
    flag = False
    q_or_not = False
    openlevelkey = False
    while runningminimap:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in connected_destinations.keys():
                    res = i.update(event)
                    if res and i in connected_destinations[current_destination]:
                        openlevelkey = roads_files[(i, current_destination)]
                        break
                    elif res and i not in connected_destinations[current_destination]:
                        print(False)
                q_or_not = quit_to_the_menu.update(event)
                if q_or_not or openlevelkey:
                    flag = True
                    break
        if flag:
            break
        clock.tick(10)
        for i in connected_destinations.keys():
            i.draw(screen)
        quit_to_the_menu.draw(screen)
        pygame.display.flip()
    if q_or_not:
        return BACK_TO_MENU
    if openlevelkey:
        return openlevelkey


def running_level(filename):
    fps = 50
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('truck.png', -1)

    tile_width = tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    def start_screen():
        intro_text = ["ЗАСТАВКА", "",
                      "Правила игры",
                      "Доехать до пункта назначения"]

        fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        clock = pygame.time.Clock()
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while True:
            for event_ in pygame.event.get():
                if event_.type == pygame.QUIT:
                    terminate()
                elif event_.type == pygame.KEYDOWN or \
                        event_.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            clock.tick(fps)

    def load_level(filename):
        filename = "data/" + filename
        try:
            with open(filename, 'r') as mapFile:
                level_map = [line.strip() for line in mapFile]
            max_width = max(map(len, level_map))
            return list(map(lambda x: x.ljust(max_width, '.'), level_map))
        except FileNotFoundError:
            val = ['.....' for i in range(5)]
            val[0] = '@....'
            return val

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            self.ismove_possible = False
            self.pos_x = pos_x
            self.pos_y = pos_y
            super().__init__(player_group, all_sprites)
            self.image = player_image
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 15, tile_height * pos_y + 5)

        def update(self, *args):
            self.ismove_possible = False
            old_x, old_y = (self.pos_x, self.pos_y)
            if args and args[0].type == pygame.KEYDOWN and \
                    args[0].key == pygame.K_LEFT:
                try:
                    if load_level(filename)[self.pos_y][self.pos_x - 1] != '#' and self.pos_x - 1 > 0:
                        self.pos_x -= 1
                except IndexError:
                    return
            elif args and args[0].type == pygame.KEYDOWN and \
                    args[0].key == pygame.K_RIGHT:
                try:
                    if load_level(filename)[self.pos_y][self.pos_x + 1] != '#':
                        self.pos_x += 1
                except IndexError:
                    return
            elif args and args[0].type == pygame.KEYDOWN and \
                    args[0].key == pygame.K_UP:
                print(1)
                try:
                    if load_level(filename)[self.pos_y - 1][self.pos_x] != '#' and self.pos_y - 1 > 0:
                        self.pos_y -= 1
                except IndexError:
                    return
            elif args and args[0].type == pygame.KEYDOWN and \
                    args[0].key == pygame.K_DOWN:
                try:
                    if load_level(filename)[self.pos_y + 1][self.pos_x] != '#':
                        self.pos_y += 1
                except IndexError:
                    return
            print((old_x, old_y), (self.pos_x, self.pos_y))
            if (old_x, old_y) != (self.pos_x, self.pos_y):
                self.ismove_possible = True

    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y

    class Camera:
        # зададим начальный сдвиг камеры
        def __init__(self):
            self.dx = 0
            self.dy = 0

        # сдвинуть объект obj на смещение камеры
        def apply(self, obj):
            obj.rect.x += self.dx
            obj.rect.y += self.dy

        # позиционировать камеру на объекте target
        def update(self, newdx, newdy):
            self.dx = newdx
            self.dy = newdy

    camera = Camera()

    player, level__x, level__y = generate_level(load_level(filename))
    start_screen()
    running = True
    time_ = pygame.time.Clock()
    while running:
        level_x, level_y = 0, 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                player.update(event)
                if event.key == pygame.K_DOWN:
                    level_y = -tile_width
                if event.key == pygame.K_UP:
                    level_y = tile_width
                if event.key == pygame.K_LEFT:
                    level_x = tile_width
                if event.key == pygame.K_RIGHT:
                    level_x = -tile_width

        if player.ismove_possible:
            camera.update(level_x, level_y)
            for sprite in tiles_group:
                camera.apply(sprite)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        time_.tick(fps)
    pygame.quit()


run_level = None
run_minimap = None
run_preview = running_preview()
run_the_first_time = False
while any((run_level, run_preview, run_minimap)):
    '''print(run_minimap, run_preview, run_level)'''
    if run_preview == SHOW_MINIMAP:
        run_minimap, run_preview = None, None
        run_minimap = running_minimap()
    elif run_minimap == BACK_TO_MENU:
        run_minimap, run_preview = None, None
        run_preview = running_preview()
    elif isinstance(run_minimap, str):
        print(run_minimap)
        run_level = running_level(run_minimap)
    elif run_preview == EXIT_FROM_GAME or run_minimap == EXIT_FROM_GAME:
        pygame.quit()
        break