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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def get_cur_frame(self):
        return self.image

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class End(pygame.sprite.Sprite):
    image = load_image("gameover.png")

    def __init__(self, distance, dest, *group, win=True):
        super().__init__(*group)
        self.c = 0
        self.image = End.image
        if win:
            self.salut = AnimatedSprite(load_image('salut.jpg', -1), 3, 3, 150, 150)
        self.rect = self.image.get_rect()
        self.rect.x = -600
        self.rect.y = 0
        font = pygame.font.Font('Australianflyingcorpsstencilsh.ttf', 30)
        string_rendered = font.render(distance, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 154
        intro_rect.y = 358
        self.image.blit(string_rendered, intro_rect)
        string_rendered = font.render(str(dest), True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 238
        intro_rect.y = 401
        self.image.blit(string_rendered, intro_rect)

    def update(self, *args):
        self.c += 1
        self.c //= 5
        if self.c % 5 == 0:
            self.salut.update()
            self.image.blit(self.salut.get_cur_frame(), (0, 0))
        if self.rect.x != 0:
            self.rect = self.rect.move(1, 0)


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
                if event.key == pygame.K_a:
                    pygame.mixer.music.pause()
                elif event.key == pygame.K_q:
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
        pygame.mixer.music.stop()
        return SHOW_MINIMAP
    if res1:
        return EXIT_FROM_GAME


def running_minimap():
    fps = 50

    def start_screen():
        intro_text = ['Выберите начальную точку:',
                      ' moscow: 1',
                      'kazan: 2',
                      'saratov: 3',
                      'samara: 4',
                      'tyla: 5', 'penza: 6', 'piter: 7']

        fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 0
        time_count = pygame.time.Clock()
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
                    if event_.key == pygame.K_1:
                        return '1'
                    if event_.key == pygame.K_2:
                        return '2'
                    if event_.key == pygame.K_3:
                        return '3'
                    if event_.key == pygame.K_4:
                        return '4'
                    if event_.key == pygame.K_5:
                        return '5'
                    if event_.key == pygame.K_6:
                        return '6'
                    if event_.key == pygame.K_7:
                        return '7'
            pygame.display.flip()
            time_count.tick(fps)
    size = width, height = 550, 690
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('simulator truck')
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
    if run_the_first_time:
        current_destination = (start_screen())
    else:
        current_destination = (start_screen())
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
    screen.fill((0, 0, 0))
    bg = pygame.image.load("Roads.png")
    screen.blit(bg, (0, 0))
    while runningminimap:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in connected_destinations.keys():
                    res = i.update(event)
                    if res and i in connected_destinations[current_destination]:
                        openlevelkey = (roads_files[(i, current_destination)], i.text, current_destination.text)
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
    moveable = ('R', '#')
    finish_coord = (0, 0)
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png'),
        'emptyF': load_image('grass_fin.png'),
        'rock': load_image('rock.png'),
        'lava': load_image('lava.png')
    }
    player_image = load_image('truck1.png', -1)

    tile_width = tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    def start_screen():
        intro_text = ["ЗАСТАВКА", "",
                      "Правила игры",
                      "Доехать до пункта назначения,",
                      "и не умереть!!!!!"]

        fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        clock = pygame.time.Clock()
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
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

    def end_screen(dist, destination_):
        allsprites = pygame.sprite.Group()
        runing = True
        pygame.mixer.music.load('data/intro lobby.mp3')
        pygame.mixer.music.play(-1)
        End(dist, destination_, allsprites)
        while runing:
            for event_1 in pygame.event.get():
                if event_1.type == pygame.QUIT:
                    runing = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        pygame.mixer.music.pause()
                    elif event.key == pygame.K_d:
                        pygame.mixer.music.unpause()
            allsprites.update()
            allsprites.draw(screen)
            pygame.display.flip()
            time_.tick(fps)
        pygame.mixer.music.stop()
        pygame.quit()

    def load_level(file_name):
        file_name = "data/" + file_name
        try:
            with open(file_name, 'r') as mapFile:
                level_map = [line.strip() for line in mapFile]
            max_width = max(map(len, level_map))
            return list(map(lambda x: x.ljust(max_width, '.'), level_map))
        except FileNotFoundError:
            val = ['.....' for _ in range(5)]
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
            self.current_moves = 0
            self.image = player_image
            self.rect = self.image.get_rect().move(
                tile_width * pos_x - 5, tile_height * pos_y + 22)
            self.lvl_map = load_level(filename[0])

        def get_coords(self):
            return self.pos_x, self.pos_y

        def get_distance(self):
            return self.current_moves

        def find_wall(self, x, y):
            try:
                if self.lvl_map[y][x - 1] in moveable and x - 1 > 0:
                    return True
            except IndexError:
                pass
            try:
                if self.lvl_map[y][x + 1] in moveable:
                    return True
            except IndexError:
                pass
            try:
                if self.lvl_map[y + 1][x + 1] in moveable:
                    return True
            except IndexError:
                pass
            try:
                print(self.lvl_map[y + 1][x - 1])
                if self.lvl_map[y + 1][x - 1] in moveable and x - 1 > 0:
                    return True
            except IndexError:
                pass
            try:
                if self.lvl_map[y + 1][x] in moveable:
                    return True
            except IndexError:
                pass
            return False

        def func(self, old_x, old_y):
            if (old_x, old_y) != (self.pos_x, self.pos_y):
                self.current_moves += 1
                self.ismove_possible = True

        def update(self, *args):
            self.ismove_possible = False
            old_x, old_y = (self.pos_x, self.pos_y)
            if args and args[0].type == pygame.KEYDOWN and \
                    args[0].key == pygame.K_LEFT:
                try:
                    if (self.lvl_map[self.pos_y][self.pos_x - 1] not in moveable and self.pos_x - 1 > 0
                            and self.find_wall(self.pos_x - 1, self.pos_y)):
                        self.pos_x -= 1
                except IndexError:
                    return
                self.func(old_x, old_y)
                return
            if args and args[0].type == pygame.KEYDOWN and \
                    args[0].key == pygame.K_RIGHT:
                try:
                    if (self.lvl_map[self.pos_y][self.pos_x + 1] not in moveable
                            and self.find_wall(self.pos_x + 1, self.pos_y)):
                        self.pos_x += 1
                except IndexError:
                    return
                self.func(old_x, old_y)
                return
            if args and args[0].type == pygame.KEYDOWN and \
                    args[0].key == pygame.K_UP:
                try:
                    if (self.lvl_map[self.pos_y - 1][self.pos_x] not in moveable and self.pos_y - 1 > 0
                            and self.find_wall(self.pos_x, self.pos_y - 1)):
                        self.pos_y -= 1
                except IndexError:
                    return
                self.func(old_x, old_y)
                return
            if args and args[0].type == pygame.KEYDOWN and \
                    args[0].key == pygame.K_DOWN:
                try:
                    if (self.lvl_map[self.pos_y + 1][self.pos_x] not in moveable
                            and self.find_wall(self.pos_x, self.pos_y + 1)):
                        self.pos_y += 1
                except IndexError:
                    return
                self.func(old_x, old_y)
                return

    def generate_level(level):
        nonlocal finish_coord
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
                elif level[y][x] == 'F':
                    finish_coord = (x, y)
                    Tile('emptyF', x, y)
                elif level[y][x] == 'R':
                    Tile('rock', x, y)
                elif level[y][x] == '*':
                    Tile('lava', x, y)
                else:
                    Tile('empty', x, y)
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

    player, level__x, level__y = generate_level(load_level(filename[0]))
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
                print(player.get_coords(), finish_coord)
        if player.ismove_possible:
            camera.update(level_x, level_y)
            for sprite in tiles_group:
                camera.apply(sprite)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        if player.get_coords() == finish_coord:
            break
        pygame.display.flip()
        time_.tick(fps)
    end_screen(str(player.get_distance()), filename[1])
    pygame.quit()


run_level = None
run_minimap = None
run_preview = running_preview()
run_the_first_time = True
while any((run_level, run_preview, run_minimap)):
    '''print(run_minimap, run_preview, run_level)'''
    if run_preview == SHOW_MINIMAP:
        run_minimap, run_preview = None, None
        run_minimap = running_minimap(run_the_first_time)
    elif run_minimap == BACK_TO_MENU:
        run_minimap, run_preview = None, None
        run_preview = running_preview()
    elif isinstance(run_minimap, tuple):
        run_level = running_level(run_minimap)
    elif run_preview == EXIT_FROM_GAME or run_minimap == EXIT_FROM_GAME:
        pygame.quit()
        break
    run_the_first_time = True
