import sys
import random
from math import log
import pygame
from pygame.math import Vector2
import pathlib
pygame.init()
current_path = pathlib.Path(__file__).parent


from player import Player
from enemy import Enemy
from menu import Menu

class Game():
    def __init__(self):
        # window setings--------------------------------------------------------------------------------
        self.size = (1280, 720)
        self.window = pygame.display.set_mode(self.size)
        self.title = "Space invadors clone"
        self.icon = pygame.image.load(current_path/'img/ufo.png')  # Icons made by Freepik www.flaticon.com
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)
        self.img_background = pygame.image.load(current_path/'img/stardust_@2X.png')  # Background pattern from Toptal Subtle Patterns
        self.img_background = pygame.transform.scale(self.img_background, self.size)
        self.window.blit(self.img_background, (0, 0))
        self.runing = True
        
        # level and lives-------------------------------------------------------------------------------
        self.level = 0
        self.level_ticks = 2400  # ticks to level up
        self.level_clock = self.level_ticks
        self.lives = 5
        self.MAIN_FONT = pygame.font.SysFont("Comic Sans", 50)
        
        # objects initialisation------------------------------------------------------------------------
        self.player = Player(self)
        self.enemy_vel = Vector2(0, log((self.level + 1), 2) // 3 + 1)
        self.enemy_bullets_vel = 2 * self.enemy_vel
        self.enemy = Enemy(self, Vector2(0, 0))
        self.enemys = []
        self.bullets = []

        # spawning-------------------------------------------------------------------------------------
        self.spawn_i = -1
        self.to_spawn = []
        self.spawn_ticks_base = 200  # plus randint(-60, 60) it's number of ticks between spawns
        self.spawn_clock = 0
        
        # atacking-------------------------------------------------------------------------------------
        self.attack_ticks_base = 200  # plus randint(-60, 60) it's number of ticks between attacks
        self.attack_clock = self.attack_ticks_base
        
        option = Menu(self, "Main menu", ("Play", "Exit")).choice()
        if option == 0: pass
        else: sys.exit(0)
        
        # time-----------------------------------------------------------------------------------------
        self.delta = 0.0
        self.tps_max = 120
        self.clock = pygame.time.Clock()
        
        # game loop------------------------------------------------------------------------------------
        while self.runing:
            # handle events----------------------------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                
            # ticking----------------------------------------------------------------------------------
            self.delta += self.clock.tick() / 1000.0
            while self.delta >= 1 / self.tps_max:
                self.delta -= 1 / self.tps_max
                self.tick()
                    
            # drawing----------------------------------------------------------------------------------
            self.window.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            
            
    def enemy_spawn(self):
        # random sequence of spawn places--------------------------------------------------------------
        if self.spawn_i < 0:
            self.to_spawn = random.sample(range(4), 4)
            self.spawn_i = 3
        
        # random x position inside choosen place and spawning new enemy--------------------------------
        new_enemy_x = ((self.size[0] - 20) // 4) * self.to_spawn[self.spawn_i] + random.randint(self.enemy.width, (((self.size[0] - 20) // 4) - self.enemy.width)) + 10
        new_enemy = Enemy(self, Vector2(new_enemy_x, -self.enemy.height))
        self.enemys.append(new_enemy)
        self.spawn_i -= 1
        
    def enemy_attack(self):
        try:
            # choosing witch enemy atacks-------------------------------------------------------------------
            delta_pos_min = 100000  # big valeu, just for sure that ther will by smaller value in loop bellow
            for enemy in self.enemys:
                if self.player.acc == 0: delta_pos = abs(self.player.pos.x - enemy.pos.x)
                else: delta_pos = self.player.acc * (self.player.pos.x - enemy.pos.x)
                if delta_pos_min > delta_pos:
                    delta_pos_min = delta_pos
                    attacking_enemy = enemy
                    
            attacking_enemy.attack()
        except: pass
        
    def tick(self):
        # objects ticks---------------------------------------------------------------------------------
        self.player.tick()
        for bullet in self.bullets: bullet.tick()
        for enemy in self.enemys: enemy.tick()
        
        # level up--------------------------------------------------------------------------------------
        self.level_clock -= 1
        if self.level_clock <= 0:
            self.level += 1
            self.level_clock = self.level_ticks
            self.enemy_vel = Vector2(0, log((self.level + 1), 2) // 1.5 + 1)
            self.enemy_bullets_vel = 2 * self.enemy_vel
            
        # spawning--------------------------------------------------------------------------------------
        self.spawn_clock -= 1
        if self.spawn_clock <= 0:
            self.enemy_spawn()
            self.spawn_clock = self.spawn_ticks_base + random.randint(-60, 60)
            
        # attacking------------------------------------------------------------------------------------
        self.attack_clock -= 1
        if self.attack_clock <= 0:
            self.enemy_attack()
            self.attack_clock = self.attack_ticks_base + random.randint(-60, 60)
        
        # loseing--------------------------------------------------------------------------------------
        if self.lives < 1:
            if Menu(self, 'Game Over!', ('Main menu', 'Exit')).choice() == 1:
                self.runing = False
            else: self.__init__()

    def draw(self):
        # background-----------------------------------------------------------------------------------
        self.window.blit(self.img_background, (0, 0))
        
        # sprites--------------------------------------------------------------------------------------
        self.player.draw()
        for bullet in self.bullets: bullet.draw()
        for enemy in self.enemys: enemy.draw()
        
        # level and lives------------------------------------------------------------------------------
        lives_label = self.MAIN_FONT.render(f"Lives: {self.lives}", 1, (255, 255, 255))
        level_label = self.MAIN_FONT.render(f"Level: {self.level}", 1, (255, 255, 255))
        self.window.blit(lives_label, (10, 10))
        self.window.blit(level_label, (10, 50))
        
Game()
