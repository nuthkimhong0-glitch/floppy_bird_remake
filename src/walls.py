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
        self.__Nblocks = global_variable.GLOBAL_NUM_DIVIDE_HOLE
        self.__sY = 300
        self.__pY = global_variable.SCREEN_SIZE_Y / self.__Nblocks
        self.__pY_1 = self.__pY + self.__sY
        
        
        
        #confug the point of pos (triagle)
        self.__gap = 30*math.sqrt(2)
        self.__onXU = 50
        self.__onYU = 50
        self.__poX1 = [self.__onXU,(self.__onXU + self.__onXU * 3)/2,self.__onXU*3]
        self.__poY1 = [self.__onYU,self.__onYU*2,self.__onYU]
        self.__poY2 = [self.__onYU*3,self.__onYU*2,self.__onYU*3]
        
        # self.__variable_a = math.sqrt((((self.__poX1[0]+self.__poX1[2])/2)**2) + (self.__poY2[1]-self.__poY2[0])**2)
        self.__offSetX = math.sqrt(((self.__gap*math.sin(45))**2) + (self.__gap**2));
        # print(self.__variable_a)
        print(self.__offSetX)
    def update(self):
        self.__lowwer_render()
        self.__upper_render()
        
    def __upper_render(self):
        pygame.draw.polygon(self.screen,(50,50,0),[(self.__poX1[0]+self.__offSetX, self.__poY1[0]),(self.__poX1[1]+self.__offSetX,self.__poY1[1]),(self.__poX1[2]+self.__offSetX,self.__poY1[2])])

    def __lowwer_render(self):
        pygame.draw.polygon(self.screen,(50,50,0),[(self.__poX1[0],self.__poY2[0]),(self.__poX1[1],self.__poY2[1]),(self.__poX1[2],self.__poY2[2])])