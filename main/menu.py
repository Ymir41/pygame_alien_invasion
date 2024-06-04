import sys
import pygame

current_path = 'D:\home\Documents\projekty python\pygame_space_invadors\main\\'

class Menu():
    def __init__(self, game, titel, options):
        self.game = game
        self.MAIN_FONT = pygame.font.SysFont('Comic Sans', 80)
        self.BUTTON_FONT = pygame.font.SysFont('Comic Sans', 50)
        self.label = self.MAIN_FONT.render(titel, 1, (200, 200, 200))
        self.button = Button(self, "", 0)
        
        # position--------------------------------------------------------------------------------------
        # label and menu
        lebel_height = self.label.get_height()
        buttons_height = len(options) * (self.button.height + 20)
        self.height = lebel_height + 10 + buttons_height
        lebel_y = self.game.size[1] // 2 - self.height // 2
        label_x = self.game.size[0] // 2 - self.label.get_width() // 2
        self.label_pos = (label_x, lebel_y)
        # buttons
        buttons_y = []
        button0_y = lebel_y + lebel_height + 30
        button_last_y = button0_y + buttons_height - 20
        for i in range(button0_y, button_last_y, self.button.height + 20):
            buttons_y.append(i)
        self.buttons = []
        for i, option in enumerate(options): self.buttons.append(Button(self, option, buttons_y[i]))
        
        # mouse-----------------------------------------------------------------------------------------
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_click = False
        self.mouse_down = False
        
        # time-----------------------------------------------------------------------------------------
        self.delta = 0.0
        self.tps_max = 120
        self.clock = pygame.time.Clock()
        
    def choice(self):
        # main loop-------------------------------------------------------------------------------------
        while True:
            # handle events----------------------------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: self.mouse_down = True
                else:  self.mouse_down = False
                if event.type == pygame.MOUSEBUTTONUP: self.mouse_click = True
                else:  self.mouse_click = False
            
            # ticking----------------------------------------------------------------------------------
            self.delta += self.clock.tick() / 1000.0
            while self.delta >= 1 / self.tps_max:
                self.delta -= 1 / self.tps_max
                self.mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button.tick(): return i
                
            # drawing---------------------------------------------------------------------------------------
            self.draw()
            pygame.display.flip() 
    
    def draw(self):
        self.game.window.blit(self.label, self.label_pos)
        for button in self.buttons: button.draw()

class Button():
    def __init__(self, menu, label, y):
        # button----------------------------------------------------------------------------------------
        self.menu = menu
        self.color_main = (200, 200, 200)
        self.color_hover = (150, 150, 150)
        self.color_active = (100, 100, 100)
        self.color = self.color_main
        self.height = 100
        self.width = 300
        x = self.menu.game.size[0] / 2 - self.width / 2
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # label-----------------------------------------------------------------------------------------
        self.label = self.menu.BUTTON_FONT.render(label, 1, (0, 0, 0))
        self.label_width = self.label.get_width()
        self.label_height = self.label.get_height()
        label_x = x + self.width / 2 - self.label_width / 2
        label_y = y + self.height / 2 - self.label_height / 2
        self.label_pos = (label_x, label_y)
        
    def tick(self):
        if self.rect.collidepoint(self.menu.mouse_pos[0], self.menu.mouse_pos[1]):
            if self.menu.mouse_down: self.color = self.color_active
            elif self.menu.mouse_click: return True
            elif not self.color == self.color_active: self.color = self.color_hover
        else: self.color = self.color_main
        return False
        
    def draw(self):
        pygame.draw.rect(self.menu.game.window, self.color, self.rect)
        self.menu.game.window.blit(self.label, self.label_pos)
        pygame.display.flip()
