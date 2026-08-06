import pygame
import random
import global_variable

class lead:
    def __init__(self,screen):
        self.is_game_pause = False
        self.screen = screen
        self.pX =0
        
    def update(self):
        if not self.is_game_pause:
            self.pX -= global_variable.GLOBAL_SPEED_X
        pygame.draw.rect(self.screen,(100,55,50),(self.pX,0,10,720))
        
class normal_wall:
    def __init__(self,Screen):
        self.is_game_pause = False
        self.__Nblocks = global_variable.GLOBAL_NUM_DIVIDE_HOLE
        self.__pos_block_y = global_variable.SCREEN_SIZE_Y / self.__Nblocks        
        self.__random_block = random.randrange(0,self.__Nblocks)
        
        self.screen = Screen
        self.pX = global_variable.SCREEN_SIZE_X *0
        self.__pY = global_variable.SCREEN_SIZE_Y
        self.sizeX = 50
        self.__sizeY = self.__random_block * self.__pos_block_y
        
        self.__vX = global_variable.GLOBAL_SPEED_X
        self.ishold = True
        
        self.__hole_pos =  self.__random_block * self.__pos_block_y + self.__pos_block_y
        self.upper_rect = pygame.Rect(self.pX,0,self.sizeX,self.__sizeY)
        self.lowwer_rect = pygame.Rect((self.pX,self.__hole_pos,self.sizeX, global_variable.SCREEN_SIZE_Y))
        
        
    def update(self):
        # print(self.__random_block)
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_e]:
        #     if self.ishold:
        #         self.reset()
        #         self.ishold = False
        # else:
        #     self.ishold = True
        if not self.is_game_pause :
            self.pX -= self.__vX
        self.__upper_wall()
        self.__lowwer_wall()
            
    def __upper_wall(self):
        self.upper_rect = pygame.Rect(self.pX,0,self.sizeX,self.__sizeY)
        pygame.draw.rect(self.screen,(0,255,100),self.upper_rect)
    
    def __lowwer_wall(self):
        self.lowwer_rect = pygame.Rect((self.pX,self.__hole_pos,self.sizeX, global_variable.SCREEN_SIZE_Y))
        pygame.draw.rect(self.screen,(0,50,0),self.lowwer_rect)
            
    
class narrow_wall:
    def __init__(self,Screen):
        self.is_game_pause = False
        self.__Nblocks = global_variable.GLOBAL_NUM_DIVIDE_HOLE
        self.__pos_block_y = global_variable.SCREEN_SIZE_Y / self.__Nblocks        
        self.__random_block = random.randrange(0,self.__Nblocks)
        
        self.screen = Screen
        self.pX = global_variable.SCREEN_SIZE_X*0
        self.__pY = global_variable.SCREEN_SIZE_Y
        self.sizeX = 1000
        self.__sizeY = self.__random_block * self.__pos_block_y
        
        self.__vX = global_variable.GLOBAL_SPEED_X
        self.ishold = True
        
        self.__hole_pos =  self.__random_block * self.__pos_block_y + self.__pos_block_y
        self.upper_rect = pygame.Rect(self.pX,0,self.sizeX,self.__sizeY)
        self.lowwer_rect = pygame.Rect((self.pX,self.__hole_pos,self.sizeX, global_variable.SCREEN_SIZE_Y))
    def update(self):
        self.__upper_wall()
        self.__lowwer_wall()
        if not self.is_game_pause :
            self.pX -= self.__vX

            
    def __upper_wall(self):
        self.upper_rect = pygame.Rect(self.pX,0,self.sizeX,self.__sizeY)
        pygame.draw.rect(self.screen,(0,255,100),self.upper_rect)
    
    def __lowwer_wall(self):
        self.lowwer_rect = pygame.Rect((self.pX,self.__hole_pos,self.sizeX, global_variable.SCREEN_SIZE_Y))
        pygame.draw.rect(self.screen,(0,50,0),self.lowwer_rect)


class triangle_wall:
    def __init__(self,Screen,scale):
        self.screen = Screen
        self.is_game_pause = False
        self.pX = global_variable.SCREEN_SIZE_X*0
        #confug the point of pos (triagle)
        self.scale = scale #from 8 to 14 gap shall small, if 15n it's close, (based on 720p, idk how to do dynamic scale yet)
        self.n_of_triagle = 2
        self.__onXU = 50
        self.__onYU = 50
        
        #ai here cuz i cant do it properly 
        # Calculate the distances relative to the starting point, then multiply by scale
        self.poX = [
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
        self.__pY = -self.__onYU
        self.offSetX = self.poX[1] 
        self.poX_shift = [x + self.offSetX - self.__onXU for x in self.poX]
        self.poX = [x - self.__onXU for x in self.poX]
        
        self.__poY = [y + self.__pY for y in self.__poY]
        self.__poY_flip = [y + self.__pY - hight for y in self.__poY_flip]
        self.__poY_flip = [y + (global_variable.SCREEN_SIZE_Y - self.__poY_flip[0])  for y in self.__poY_flip]
        
        self.size_x = self.poX[2] - self.poX[0]
        self.on_continue()


    def on_continue(self):
        self.__pos_u = [(self.poX_shift[0], self.__poY[0]),(self.poX_shift[1],self.__poY[1]),(self.poX_shift[2],self.__poY[2])]
        self.__pos_l = [(self.poX[0],self.__poY_flip[0]),(self.poX[1],self.__poY_flip[1]),(self.poX[2],self.__poY_flip[2])]
        
    def update(self):
        self.__lowwer_render()
        self.__upper_render()
        if not self.is_game_pause:
            self.__move_across_screen()
        
    def __move_across_screen(self):
        self.poX = [x-self.__vx for x in self.poX]
        self.poX_shift = [x-self.__vx for x in self.poX_shift]
        self.on_continue()
        
    def __upper_render(self):
        pygame.draw.polygon(self.screen,(50,50,0),self.__pos_u)

    def __lowwer_render(self):
        pygame.draw.polygon(self.screen,(50,50,0), self.__pos_l)
        
    def collision(self):
        pass
            