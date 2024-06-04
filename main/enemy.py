import pygame
from pygame.math import Vector2
import pathlib
pygame.init()

from player import collision

current_path = pathlib.Path(__file__).parent

IMG_ENEMY = pygame.image.load(current_path/'img/ufo.png')  # Image made by Freepik from www.flaticon.com
IMG_ENEMY_BULLET = pygame.image.load(current_path/'img/eye-ball.png')  # Image made by Freepik from www.flaticon.com 

class Enemy():
    def __init__(self, game, pos):
        self.game = game
        self.img = IMG_ENEMY
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.pos = pos
        self.vel = self.game.enemy_vel       
        
    def tick(self):
        self.pos += self.vel
        self.collisions()
        if self.pos.y > self.game.size[1]:
            self.game.lives -= 1
            self.game.enemys.remove(self)
        
    def attack(self):
        self.game.bullets.append(Bullet(self.game, Vector2(self.pos.x + self.width / 2, self.pos.y + self.height / 2)))
        
    def collisions(self):
        if collision(self, self.game.player):
            self.game.lives -= 1
            self.game.enemys.remove(self)
            
        
    def draw(self):
        self.game.window.blit(self.img, self.pos)
        
class Bullet(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.vel = self.game.enemy_bullets_vel
        self.img = IMG_ENEMY_BULLET
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.pos.x -= self.width / 2  # center of its enemy
        
    def tick(self):
        self.pos += self.vel
        self.collisions()
        if self.pos.y > self.game.size[1]:
            self.game.bullets.remove(self)
    
    def attack(self):
        pass
    
    def collisions(self):
        if collision(self, self.game.player):
            self.game.player.hp -= 1
            self.game.bullets.remove(self)
