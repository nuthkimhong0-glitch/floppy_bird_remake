import pygame
import global_variable

class bird_body:
    
    def __init__(self,Screen):
        self.screen = Screen
        self.is_game_pause = False
        
        self.__pX = global_variable.SCREEN_SIZE_X - (global_variable.SCREEN_SIZE_X * (1-0.15))
        self.__py= global_variable.SCREEN_SIZE_Y/2
        self.__sizeX = 30
        self.__sizeY = 30
        
        self.__gravity = 0.1
        self.__jump_force = 2
        self.__v_y = 0
        
        self.__is_hold = True
        self.__rect = pygame.Rect(self.__pX,self.__v_y,self.__sizeX,self.__sizeY)
    ### ai code here
        self.mask = pygame.Mask((self.__sizeX, self.__sizeY))
        self.mask.fill()

    def get_mask_data(self):
        """Returns (pygame.Mask, (x_position, y_position))"""
        return self.mask, (self.__pX, self.__py)
    ### end here
    def update(self):
        if not self.is_game_pause:
            self.__input()
            self.boundery()
        self.render()
        
    def __input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.__is_hold: 
                self.__v_y -= self.__jump_force
                self.__is_hold = False
        else:
            self.__is_hold = True

        self.__v_y += self.__gravity
        self.__py += self.__v_y
            
    
    def boundery(self):
        if self.__py < 0:
            self.__py = 0
            self.__v_y = 0
        elif self.__sizeY + self.__py > global_variable.SCREEN_SIZE_Y:
            self.__py = global_variable.SCREEN_SIZE_Y-self.__sizeX
            self.__v_y = 0
    
    def render(self):
        pygame.draw.rect(self.screen,(255,0,0),self.rect_collision_point())
        
    def rect_collision_point(self):
        self.__rect = pygame.Rect(self.__pX,self.__py,self.__sizeX,self.__sizeY)
        return self.__rect
        
        
