import pygame

class AnimatePlayer(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.idle_animation = False
        self.right_walk_animation = False
        self.left_walk_animation = False
        self.sprites_idle = []
        self.sprites_walk = []
        self.sprites_idle.append(pygame.image.load('./Assets/tile000.png'))
        self.sprites_idle.append(pygame.image.load('./Assets/tile001.png'))
        for number in range(16, 19):
            self.sprites_walk.append(pygame.image.load(f'./Assets/tile0{number}.png'))
        self.current_sprite_idle = 0
        self.current_sprite_walk = 0
        self.image = self.sprites_idle[0]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]

    def walking(self, direction):
        if direction == "right":
            self.idle_animation = False
            self.right_walk_animation = True
            self.left_walk_animation = False
        elif direction == "left":
            self.idle_animation = False
            self.right_walk_animation = False
            self.left_walk_animation = True
        else:
            self.idle_animation = True
            self.right_walk_animation = False
            self.left_walk_animation = False

    def update(self):
        if self.idle_animation:
            self.current_sprite_idle += 0.05
            if int(self.current_sprite_idle) >= len(self.sprites_idle):
                self.current_sprite_idle = 0
            self.image = self.sprites_idle[int(self.current_sprite_idle)]
        if self.right_walk_animation or self.left_walk_animation:
            self.current_sprite_walk += 1
            if self.current_sprite_walk >= len(self.sprites_walk):
                self.current_sprite_walk = 0
            self.image = self.sprites_walk[self.current_sprite_walk]
        if self.left_walk_animation:
            self.image = pygame.transform.flip(self.image, True, False)