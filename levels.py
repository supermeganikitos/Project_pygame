import pygame
import sys
import os

FPS = 50
pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
FILENAME = input('введите имя файла').strip()


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


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('truck.png', -1)

tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
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
        clock.tick(FPS)


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
                if load_level(FILENAME)[self.pos_y][self.pos_x - 1] != '#' and self.pos_x - 1 > 0:
                    self.pos_x -= 1
            except IndexError:
                return
        elif args and args[0].type == pygame.KEYDOWN and \
                args[0].key == pygame.K_RIGHT:
            try:
                if load_level(FILENAME)[self.pos_y][self.pos_x + 1] != '#':
                    self.pos_x += 1
            except IndexError:
                return
        elif args and args[0].type == pygame.KEYDOWN and \
                args[0].key == pygame.K_UP:
            try:
                if load_level(FILENAME)[self.pos_y - 1][self.pos_x] != '#' and self.pos_y - 1 > 0:
                    self.pos_y -= 1
            except IndexError:
                return
        elif args and args[0].type == pygame.KEYDOWN and \
                args[0].key == pygame.K_DOWN:
            try:
                if load_level(FILENAME)[self.pos_y + 1][self.pos_x] != '#':
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

player, level__x, level__y = generate_level(load_level(FILENAME))
start_screen()
running = True
time_ = pygame.time.Clock()
while running:
    level_x, level_y = 0, 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
    time_.tick(FPS)
pygame.quit()
