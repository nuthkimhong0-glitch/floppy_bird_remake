import global_variable
import walls
import bird
import pygame

class Mbird: # Mehcanic bird    
    def __init__(self,Screen):
        self.screen = Screen
        
        self.__pX = global_variable.SCREEN_SIZE_X - (global_variable.SCREEN_SIZE_X * (1-0.15))
        self.__py= global_variable.SCREEN_SIZE_Y/2
        self.__sizeX = 30
        self.__sizeY = 30
        
        self.__gravity = 0.1
        self.__jump_force = 2
        self.__v_y = 0
        
        self.__is_hold = True
        
        self.b = bird.bird_body(self.screen)
    
    def update(self):
        self.__input()
        self.b.render(self.__pX,self.__phys(),self.__sizeX,self.__sizeY)
        self.boundery()
        
    
    def __input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.__is_hold: 
                self.__v_y -= self.__jump_force
                self.__is_hold = False
        else:
            self.__is_hold = True
            
    def __phys(self):
        self.__v_y += self.__gravity
        self.__py += self.__v_y
        return self.__py
    
    def boundery(self):
        if self.__py < 0:
            self.__py = 0
            self.__v_y = 0
        elif self.__sizeY + self.__py > global_variable.SCREEN_SIZE_Y:
            self.__py = global_variable.SCREEN_SIZE_Y-self.__sizeX
            self.__v_y = 0
    
    
class MWall:
    def __init__(self,Screen):
        self.Nobjects = 3
        self.__walls = [walls.normal_wall(Screen) for _ in range(self.Nobjects)]
        self.__narrow_wall = walls.narrow_wall(Screen)
        self.__tri_wall = walls.triangle_wall(Screen)
        self.__on_start()
        
    def update(self):
        # self.__wall_handle()
        # self.__narrow_wall_handle();
        self.__tri_wall.update()
    
    
    # def __switch_turn(self):
        
    
    
    def __narrow_wall_handle(self):
        self.__narrow_wall.update()
        if(self.__narrow_wall.pX+ self.__narrow_wall.sizeX < 0):
            self.__narrow_wall.reset()
    
    
    
    #ts below is ai cuz im dumb af
    def __on_start(self,spacing = None):
        # spacing in pixels between walls; default to screen width / Nobjects
        self.spacing = spacing if spacing is not None else global_variable.SCREEN_SIZE_X / self.Nobjects

        
        # initial placement: all off the right edge with spacing
        for i in range(self.Nobjects):
            self.__walls[i].pX = global_variable.SCREEN_SIZE_X + i * self.spacing
            
        #logic me writing it
        self.__narrow_wall.pX = global_variable.SCREEN_SIZE_X + self.spacing; 
            
            
    def __wall_handle(self,is_active = True): 
        # update each wall exactly once per frame
        for wall in self.__walls:
            wall.update()

        # handle resets after all updates so rightmost is computed from current frame
        rightmost = max(w.pX for w in self.__walls)
        min_respawn_x = global_variable.SCREEN_SIZE_X 
        for wall in self.__walls:
                if wall.pX <= -wall.sizeX:
                    wall.reset()
                    # place after the rightmost wall but never less than min_respawn_x
                    new_x = max(rightmost + self.spacing, min_respawn_x)
                    # optional tiny jitter to avoid perfect alignment
                    # new_x += random.uniform(0, 5)
                    wall.pX = new_x
                    # update rightmost so subsequent resets chain correctly this frame
                    rightmost = wall.pX
            