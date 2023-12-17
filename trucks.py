import pygame

all_sprites = pygame.sprite.Group()


class SimpleButton(pygame.sprite.Sprite): # от него будем наследовать все кнопки и destination тоже
    pass

class Truck:
    def __init__(self):
        pass

    def func(self):
        pass


class Destination(pygame.sprite.Sprite): # Ты наследовал спрайт от группы спрайтов я это исправил
    def __init__(self):
        super().__init__(all_sprites)

    def what_check_in_this(self):
        self.dict_of_changes = [] # словарь где по ключу (части авто) будут находится изменения



