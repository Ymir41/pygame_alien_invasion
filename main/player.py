import pygame
from pygame.math import Vector2
import pathlib
pygame.init()       

current_path = pathlib.Path(__file__).parent
IMG_BULLET = pygame.image.load(current_path/'img/bullets.png')

class Player():
    def __init__(self, game):
        self.img = pygame.image.load(current_path/'img/space-ship.png')  # Image made by Good Ware from www.flaticon.com
        self.attackimg = pygame.image.load(current_path/'img/space-ship-attack.png')
        self.attacking = False
        self.cold_counter = 0  # ticks that have already gone
        self.attack_block = 30  # time that must by awaited betwean attacks (in ticks)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.game = game
        y = game.size[1] / 5 * 4 - (self.width / 2)
        x = game.size[0] / 2 - (self.width / 2)
        self.pos = Vector2(x, y)
        self.acc = 0
        self.acc_value = 3
        self.vel = 0
        self.resist = 0.7
        self.hp = 3
        self.health_bar_height = 5
        
    def draw(self):
        # player sprite----------------------------------------------------------------------------------
        if self.attacking: self.game.window.blit(self.attackimg, self.pos)
        else: self.game.window.blit(self.img, self.pos)
        
        # health bar------------------------------------------------------------------------------------
        green_length = (self.width / 3) * self.hp
        red_length = (self.width / 3) * (3 - self.hp)
        green = pygame.Rect(self.pos.x, self.pos.y + self.height, green_length, self.health_bar_height)
        pygame.draw.rect(self.game.window, (0, 255, 0), green)  # green part
        if red_length > 0:
            red = pygame.Rect(self.pos.x + green_length, self.pos.y + self.height, red_length, self.health_bar_height)
            pygame.draw.rect(self.game.window, (255, 0, 0), red)  # red part
        
    def tick(self):
        # input-----------------------------------------------------------------------------------------
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and not key[pygame.K_d]: self.acc = -self.acc_value
        elif key[pygame.K_d] and not key[pygame.K_a]: self.acc = self.acc_value
        else: self.acc = 0
        
        # attack----------------------------------------------------------------------------------------
        if self.cold_counter != 0: self.cold_counter -= 1
        if self.cold_counter == self.attack_block // 2: self.attacking = 0
        if self.cold_counter <= 0 and key[pygame.K_SPACE]:
            self.cold_counter = self.attack_block  # block nonstop attacking
            self.attack()
            
        # damages---------------------------------------------------------------------------------------
        if self.hp <= 0:
            self.hp = 3
            self.game.lives -= 1
        
        # motion----------------------------------------------------------------------------------------
        self.vel += self.acc
        self.vel *= self.resist
        
        self.pos.x += self.vel
        if self.pos.x > self.game.size[0] - self.width: self.pos.x = self.game.size[0] - self.width
        elif self.pos.x < 0: self.pos.x = 0
        
    def attack(self):
        self.attacking = True
        self.game.bullets.append(Bullet(self.game, Vector2(self.pos.x, self.pos.y)))

class Bullet():
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.vel = -10
        self.img = IMG_BULLET
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        
    def tick(self):
        self.pos.y += self.vel
        self.collisions()
        if self.pos.y < 0:
            try: self.game.bullets.remove(self)
            except: pass
        
    def draw(self):
        self.game.window.blit(self.img, self.pos)
        
    def collisions(self):
        for enemy in self.game.enemys:
            if collision(self, enemy):
                try: self.game.enemys.remove(enemy)
                except: pass
                try: self.game.bullets.remove(self)
                except: pass
        
def collision(ob1, ob2):
    if ob1.pos.x >= ob2.pos.x and ob1.pos.x <= ob2.pos.x + ob2.width and ob1.pos.y >= ob2.pos.y and ob1.pos.y <= ob2.pos.y + ob2.height:
        return True
    if ob2.pos.x >= ob1.pos.x and ob2.pos.x <= ob1.pos.x + ob1.width and ob2.pos.y >= ob1.pos.y and ob2.pos.y <= ob1.pos.y + ob1.height:
        return True
    return False
