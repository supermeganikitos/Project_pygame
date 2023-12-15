import pygame

all_sprites = pygame.sprite.Group()
class Truck:
    def __init__(self):
        pass

    def func(self):
        pass


class Destination(pygame.sprite.Group()):
    def __init__(self):
        super().__init__(all_sprites)

    def what_check_in_this(self):
        self.dict_of_changes = [] # словарь где по ключу (части авто) будут находится изменения



