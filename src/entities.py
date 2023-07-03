import pygame
import os
import src.graphics as graphics


class Player:
    def __init__(self, screen, set_state):
        self.health = 100
        self.velocity = 5
        self.direction = pygame.math.Vector2(0, 0)
        self.jump_force = -18
        self.is_in_air = True
        self.is_attack_on_cooldown = False
        self.attack_cooldown = 15
        self.can_deal_dmg = False

        self.screen = screen
        self.width, self.height = (78, 58)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.screen.get_width() / 2,
                                self.screen.get_height() / 2, self.width - 25, self.height - 10)
        
        self.hurtbox = pygame.Rect(self.screen.get_width() / 2,
                                self.screen.get_height() / 2, self.width - 15, self.height - 10)

        self.animations = {
            'idle': graphics.Animation(pygame.image.load(os.path.join('assets', 'player', 'idle.png')), (self.width, self.height), 5),
            'run': graphics.Animation(pygame.image.load(os.path.join('assets', 'player', 'run.png')), (self.width, self.height), 7),
            'jump': graphics.Animation(pygame.image.load(os.path.join('assets', 'player', 'jump.png')), (self.width, self.height), 1),
            'fall': graphics.Animation(pygame.image.load(os.path.join('assets', 'player', 'fall.png')), (self.width, self.height), 1),
            'attack': graphics.Animation(pygame.image.load(os.path.join('assets', 'player', 'attack.png')), (self.width, self.height), 5, False)
        }

        self.animation_manager = graphics.AnimationManager(self.animations)
        self.flip_sprite = False

        self.set_state = set_state

    def update(self):
        self.move()
        self.handle_cooldown()
        self.animation_manager.update()
        self.handle_hurtbox()

        if self.is_dead():
            self.set_state('lose')

    def render(self):
        # load and set correct direction of frame
        self.surface = self.animation_manager.get_current_animation().get_frame()
        self.surface.set_colorkey((0, 0, 0))

        if self.flip_sprite:
            self.surface = pygame.transform.flip(self.surface, True, False)
            self.screen.blit(self.surface, (self.rect.x - 70, self.rect.y - 40))
        else:
            self.screen.blit(self.surface, (self.rect.x - 40, self.rect.y - 40))

        # testing rects
        # block = pygame.Surface((self.rect.width, self.rect.height))
        # pygame.draw.rect(block, (255, 255, 255), self.rect)
        # self.screen.blit(block, self.rect)

        # testing hurtbox
        # block = pygame.Surface((self.hurtbox.width, self.hurtbox.height))
        # pygame.draw.rect(block, (255, 255, 255), self.hurtbox)
        # self.screen.blit(block, self.hurtbox)

    def handle_hurtbox(self):
        if self.animation_manager.state == 'attack':
            self.can_deal_dmg = True
        else:
            self.can_deal_dmg = False

        if self.flip_sprite:
            self.hurtbox.x, self.hurtbox.y = self.rect.x - self.rect.width, self.rect.y
        else:
            self.hurtbox.x, self.hurtbox.y = self.rect.x + self.rect.width, self.rect.y

    def reset_cooldown(self):
        self.attack_cooldown = 15
        self.is_attack_on_cooldown = False

    def handle_cooldown(self):
        if self.is_attack_on_cooldown:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            else:
                self.reset_cooldown()

    def is_dead(self):
        return self.health <= 0

    def gravity(self):
        self.direction.y += 0.9
        self.rect.y += self.direction.y

    def jump(self):
        self.animation_manager.set_state('jump')
        self.direction.y = self.jump_force
        self.is_in_air = True

    def attack(self):
        if not self.is_attack_on_cooldown:
            self.animation_manager.set_state('attack')
            self.is_attack_on_cooldown = True

    def move(self):
        self.rect.x += self.direction.x * self.velocity


class Enemy:
    def __init__(self, screen):
        self.health = 10
        self.velocity = 5
        self.direction = pygame.math.Vector2(0, 0)
        self.jump_force = -18
        self.is_in_air = True
        self.is_attack_on_cooldown = False
        self.attack_cooldown = 15
        self.dead = False

        self.screen = screen
        self.width, self.height = (34, 28)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.screen.get_width() / 2 + 100,
                                self.screen.get_height() / 2, self.width, self.height)

        self.animations = {
            'idle': graphics.Animation(pygame.image.load(os.path.join('assets', 'pig', 'idle.png')), (self.width, self.height), 5),
            'run': graphics.Animation(pygame.image.load(os.path.join('assets', 'pig', 'run.png')), (self.width, self.height), 7),
            'jump': graphics.Animation(pygame.image.load(os.path.join('assets', 'pig', 'jump.png')), (self.width, self.height), 1),
            'fall': graphics.Animation(pygame.image.load(os.path.join('assets', 'pig', 'fall.png')), (self.width, self.height), 1),
            'attack': graphics.Animation(pygame.image.load(os.path.join('assets', 'pig', 'attack.png')), (self.width, self.height), 5, False),
            'dead': graphics.Animation(pygame.image.load(os.path.join('assets', 'pig', 'dead.png')), (self.width, self.height), 5, False)
        }

        self.animation_manager = graphics.AnimationManager(self.animations)
        self.flip_sprite = False

    def gravity(self):
        self.direction.y += 0.9
        self.rect.y += self.direction.y

    def take_damage(self):
        self.health -= 10
    
    def is_dead(self):
        return self.dead

    def update(self):
        self.animation_manager.update()
        if self.health <= 0 and self.animation_manager.state != 'dead':
            self.animation_manager.set_state('dead')  

        if self.animation_manager.state == 'dead' and self.animation_manager.animation_status == 'done':
            self.dead = True

    def render(self):
        # load and set correct direction of frame
        self.surface = self.animation_manager.get_current_animation().get_frame()

        if self.flip_sprite:
            self.surface = pygame.transform.flip(self.surface, True, False)

        self.surface.set_colorkey((0, 0, 0))
        self.screen.blit(self.surface, (self.rect.x -
                         self.rect.width, self.rect.y - self.rect.height))


class Door:
    def __init__(self, state, screen, pos, change_scene=None) -> None:
        self.state = state
        self.screen = screen
        self.width, self.height = (46, 56)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(pos, (self.width * 2, self.height * 2))
        self.change_scene = change_scene

        self.animations = {
            'idle': graphics.Animation(pygame.image.load(os.path.join('assets', 'door', 'idle.png')), (self.width, self.height), 1),
            'open': graphics.Animation(pygame.image.load(os.path.join('assets', 'door', 'opening.png')), (self.width, self.height), 5, False),
            'close': graphics.Animation(pygame.image.load(os.path.join('assets', 'door', 'closing.png')), (self.width, self.height), 5, False)
        }

        self.animation_manager = graphics.AnimationManager(self.animations)
        if self.state == 'enter':
            self.animation_manager.state = 'close'

    def check_enter(self):
        if self.animation_manager.state == 'open' and self.animation_manager.animation_status == 'done':
            self.change_scene()

    def update(self):
        self.animate()

        if self.state == 'exit':
            self.check_enter()

    def render(self):
        self.surface = self.animation_manager.get_current_animation().get_frame()

        self.surface.set_colorkey((0, 0, 0))
        self.screen.blit(self.surface, (self.rect.x, self.rect.y))

    def animate(self):
        self.animation_manager.update()


class Box:
    def __init__(self, screen, position) -> None:
        self.screen = screen
        self.width, self.height = (22, 16)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.set_position(position)

        self.animations = {
            'idle': graphics.Animation(pygame.image.load(os.path.join('assets', 'box', 'idle.png')), (self.width, self.height), 1),
            'hit': graphics.Animation(pygame.image.load(os.path.join('assets', 'box', 'hit.png')), (self.width, self.height), 1),
        }
        self.animation_manager = graphics.AnimationManager(self.animations)

    def set_position(self, position):
        self.rect.x, self.rect.y = position

    def render(self):
        self.surface = self.animation_manager.get_current_animation().get_frame()

        self.surface.set_colorkey((0, 0, 0))
        self.screen.blit(self.surface, (self.rect.x, self.rect.y))

    def update(self):
        self.animation_manager.update()
        self.animate()

    def animate(self):
        self.animation_manager.set_state('idle')
