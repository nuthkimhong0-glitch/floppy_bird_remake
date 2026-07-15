import pygame
import math
import random
import global_variable

class normal_wall:
    def __init__(self,Screen):
        self.__Nblocks = global_variable.GLOBAL_NUM_DIVIDE_HOLE
        self.__pos_block_y = global_variable.SCREEN_SIZE_Y / self.__Nblocks        
        self.__random_block = random.randrange(0,self.__Nblocks)
        
        self.screen = Screen
        self.pX = global_variable.SCREEN_SIZE_X
        self.__pY = global_variable.SCREEN_SIZE_Y
        self.sizeX = 50
        self.__sizeY = self.__random_block * self.__pos_block_y
        
        self.__vX = global_variable.GLOBAL_SPEED_X
        self.ishold = True
        
    def update(self):
        # print(self.__random_block)
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_e]:
        #     if self.ishold:
        #         self.reset()
        #         self.ishold = False
        # else:
        #     self.ishold = True
            
        self.__upper_wall()
        self.__lowwer_wall()
    def __move_across_screen(self):
        self.pX -= self.__vX
        return self.pX
            
    def __upper_wall(self):
        pygame.draw.rect(self.screen,(0,255,100),(self.__move_across_screen(),0,self.sizeX,self.__sizeY))
    
    def __lowwer_wall(self):
        pos =  self.__random_block * self.__pos_block_y + self.__pos_block_y
        pygame.draw.rect(self.screen,(0,50,0),(self.__move_across_screen(),pos,self.sizeX, global_variable.SCREEN_SIZE_Y))
    
    def reset(self):
        self.__random_block = random.randrange(0,self.__Nblocks)
        self.__sizeY = self.__random_block * self.__pos_block_y
        self.pX = global_variable.SCREEN_SIZE_X
    
class narrow_wall:
    def __init__(self,Screen):
        self.__Nblocks = global_variable.GLOBAL_NUM_DIVIDE_HOLE
        self.__pos_block_y = global_variable.SCREEN_SIZE_Y / self.__Nblocks        
        self.__random_block = random.randrange(0,self.__Nblocks)
        
        self.screen = Screen
        self.pX = global_variable.SCREEN_SIZE_X
        self.__pY = global_variable.SCREEN_SIZE_Y
        self.sizeX = 1000
        self.__sizeY = self.__random_block * self.__pos_block_y
        
        self.__vX = global_variable.GLOBAL_SPEED_X
        self.ishold = True
        
    def update(self):
        self.__upper_wall()
        self.__lowwer_wall()

    def __move_across_screen(self):
        self.pX -= self.__vX
        return self.pX
            
    def __upper_wall(self):
        pygame.draw.rect(self.screen,(0,255,100),(self.__move_across_screen(),0,self.sizeX,self.__sizeY))
    
    def __lowwer_wall(self):
        pos =  self.__random_block * self.__pos_block_y + self.__pos_block_y
        pygame.draw.rect(self.screen,(0,50,0),(self.__move_across_screen(),pos,self.sizeX, global_variable.SCREEN_SIZE_Y))
    
    def reset(self):
        self.__random_block = random.randrange(0,self.__Nblocks)
        self.__sizeY = self.__random_block * self.__pos_block_y
        self.pX = global_variable.SCREEN_SIZE_X

class triangle_wall:
    def __init__(self,Screen):
        self.screen = Screen
        
        #confug the point of pos (triagle)
        self.scale = 4 #from 8 to 14 gap shall small, if 15 close, (based on 720p, idk how to do dynamic scale yet)
        self.n_of_triagle = 2
        self.__onXU = 50
        self.__onYU = 50
        
        #ai here cuz i cant do it properly 
        # Calculate the distances relative to the starting point, then multiply by scale
        self.__poX = [
            self.__onXU,                                             # Point 1: Stays at the start position
            self.__onXU + (self.scale * (self.__onXU * 2) / 2),      # Point 2: Scaled distance from Point 1
            self.__onXU + (self.scale * self.__onXU * 2)             # Point 3: Scaled distance from Point 1
        ]

        self.__poY = [
            self.__onYU,                                             # Point 1: Stays at the start position
            self.__onYU + (self.scale * self.__onYU),                # Point 2: Scaled distance from Point 1
            self.__onYU                                              # Point 3: Returns to start Y position
        ]
        #end here
        
        hight = self.__poY[1] - self.__poY[0]
        self.__poY_flip = [(self.__poY[0]+self.__poY[2] - y) + hight * 2  for y in self.__poY] # ts so simple why cant i firgure it out lmao
        
        self.__vx = global_variable.GLOBAL_SPEED_X
        #set position
        self.__pX = 0
        self.__pY = -self.__onYU
        self.__poX = [x + self.__pX -self.__onXU for x in self.__poX]
        offSetX = self.__poX[1]
        self.__poX_shift = [x + offSetX + self.__pX  for x in self.__poX]
        
        self.__poY = [y + self.__pY for y in self.__poY]
        self.__poY_flip = [y + self.__pY - hight for y in self.__poY_flip]
        self.__poY_flip = [y + (global_variable.SCREEN_SIZE_Y - self.__poY_flip[0])  for y in self.__poY_flip]


    def update(self):
        self.__lowwer_render()
        self.__upper_render()
    
    def __move_across_screen(self):
        self.__pX -= self.__vX
        return self.pX
    
    def __upper_render(self):
        based = self.__poX_shift[2]
        fix_gap =  self.__poX_shift[2]-self.__poX_shift[1]
        temp = [(self.__poX_shift[0], self.__poY[0]),(self.__poX_shift[1],self.__poY[1]),(self.__poX_shift[2],self.__poY[2])]
        for n in range(0,self.n_of_triagle):
            pygame.draw.polygon(self.screen,(50,50,0),temp)
            temp = [(x+based - fix_gap,y) for x,y in temp]

    def __lowwer_render(self):
        based = self.__poX[2]
        temp = [(self.__poX[0],self.__poY_flip[0]),(self.__poX[1],self.__poY_flip[1]),(self.__poX[2],self.__poY_flip[2])]
        for n in range(0,self.n_of_triagle):
            pygame.draw.polygon(self.screen,(50,50,0),temp)
            temp = [(x+based,y) for x,y in temp]
            