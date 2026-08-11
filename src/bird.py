import pygame
import global_variable
class bird_body:
    
    def __init__(self,Screen,assets):
        self.screen = Screen
        self.player_asset = assets
        self.is_game_pause = False
        self.__pX = global_variable.SCREEN_SIZE_X - (global_variable.SCREEN_SIZE_X * (1-0.15))
        self.__py= global_variable.SCREEN_SIZE_Y/2
        self.__sizeX = 30
        self.__sizeY = 30
        
        self.__gravity = 0.1
        self.__jump_force = 2
        self.__v_y = 0
        
        self.__animatino_state = 0 # maximun 3 cuz have 3 frame of animation

        self.__is_held = True
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
            if self.__is_held: 
                self.__v_y -= self.__jump_force
                self.__is_held = False
        else:
            self.__is_held = True

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
        self.__animation()
        self.screen.blit(self.player_asset.images_player[int(self.__animatino_state)],self.rect_collision_point())
        # pygame.draw.rect(self.screen,(255,0,0),self.rect_collision_point())
        
    def rect_collision_point(self):
        self.__rect = pygame.Rect(self.__pX,self.__py,self.__sizeX,self.__sizeY)
        return self.__rect
    
    def __animation(self):
        print(int(self.__animatino_state))
        if self.__animatino_state < 2.9: 
            self.__animatino_state += global_variable.GLOBAL_ANIMATION_SPEED
        else:
            self.__animatino_state = 0