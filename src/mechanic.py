import global_variable
import random
import walls
import math
from bird import bird_body
import pygame

class Mbird: # Mehcanic bird    
    def __init__(self,Screen):
        self.screen = Screen
        self.b = bird_body(Screen)
    
    def update(self):
        self.b.update()
    def collision (self):
        return self.b.rect_collision_point()
class Object:
    def __init__(self,Screen,maximun_object,order):
        self.screen = Screen
        self.num_of_wall_1 = [ x+1 for x in range(maximun_object)]
        self.num_of_wall_2 = [ x+1 for x in range(maximun_object)]
        
        random.shuffle(self.num_of_wall_1)
        random.shuffle(self.num_of_wall_2)
        
        self.__lead = walls.lead(self.screen)
        self.__wallp = [walls.normal_wall(self.screen) for _ in range(self.num_of_wall_1[0])]
        self.__narrow_wall = walls.narrow_wall(self.screen) 
        self.__tri_wall = [walls.triangle_wall(self.screen,5) for _ in range(self.num_of_wall_2[0])]
        self.__rect_Gpoint = [] #G for goal?? idk what is the right name
        
        self.last_pos = 0
        self.order = order
        
    def spawn(self):
        currentX = global_variable.SCREEN_SIZE_X
        self.__lead.pX = currentX
        
        match self.order:
            case 0:
                for  i  in range(self.num_of_wall_1[0]):
                    self.__wallp[i].pX = currentX
    
                    self.__rect_Gpoint.append(pygame.Rect(self.__wallp[i].pX+self.__wallp[i].sizeX-5,0,5,720))
                    
                    currentX += global_variable.GLOBAL_SHIFT_POSITION_X_FROM_EACH_OTHER + self.__wallp[i].sizeX
            case 1:
                self.__narrow_wall.pX = currentX
                self.__rect_Gpoint.append(pygame.Rect(self.__narrow_wall.pX+self.__narrow_wall.sizeX-5,0,5,720))
                currentX += global_variable.GLOBAL_SHIFT_POSITION_X_FROM_EACH_OTHER + self.__narrow_wall.sizeX
            case 2:
                size_px = self.__tri_wall[0].size_x
                for i in range(self.num_of_wall_2[0]):
                    self.__tri_wall[i].poX = [x+currentX for x in self.__tri_wall[i].poX]
                    self.__tri_wall[i].poX_shift = [x+currentX for x in self.__tri_wall[i].poX_shift]
                    self.__tri_wall[i].on_continue()
                    currentX += size_px
                self.__rect_Gpoint.append(pygame.Rect(self.__tri_wall[-1].poX_shift[1],0,5,720))
                currentX += global_variable.GLOBAL_SHIFT_POSITION_X_FROM_EACH_OTHER + self.__tri_wall[0].offSetX

        self.last_pos = currentX - self.__tri_wall[0].offSetX *0
    
    def __which_to_spawn(self):
        if self.order == 0 :
            for w1 in self.__wallp[:]:
                w1.update()
        elif self.order == 1:
            self.__narrow_wall.update()
        elif self.order == 2:
            for t1 in self.__tri_wall[:]:
                t1.update()
            
    
    def update(self):
        
        self.__which_to_spawn()
            
        for rect in self.__rect_Gpoint:
            pygame.draw.rect(self.screen,(0,24,233),rect)
            rect.x -= global_variable.GLOBAL_SPEED_X
            
        self.last_pos -= global_variable.GLOBAL_SPEED_X
        # self.__lead.update()
    
    def score_rect_collision(self):
        return self.__rect_Gpoint     
class MWall:
    def __init__(self,Screen):
        self.screen = Screen
            
        self.score =0
        self.level_max = 5
        self.spawn_rate = [0.6,0.3,0.1]
        self.growth_rate = 0.08
        # self.__half_step = int(math.log(self.level_max)/self.growth_rate)

        self.num_of_spawn = 5
        self.__objs = []
        self.__is_hit = False
        first_obj = Object(self.screen,self.num_of_spawn,self.choose_algorithm())
        first_obj.spawn()
        self.__objs.append(first_obj)
            
    def update(self):
        self.spawn_mechanics()
        
    def spawn_mechanics(self):
        
        for obj in self.__objs:
            obj.update()
        
        if self.__objs[-1].last_pos + global_variable.GLOBAL_SHIFT_POSITION_X_FROM_EACH_OTHER < global_variable.SCREEN_SIZE_X:
            new_obj = Object(self.screen, self.num_of_spawn, self.choose_algorithm())
            new_obj.spawn()
            self.__objs.append(new_obj)
            
        if self.__objs[0].last_pos < -10:
            self.__objs.pop(0)
                
                
        
    def choose_algorithm(self):
        #i ask the ai then i got this formula, i impliment them cool
        choose_obj = [0,1,2]
        current_level = self.level_max/(1+(self.level_max-1)*math.pow(math.e,-self.growth_rate*self.score))
        
        probab = (current_level - 1)/ (self.level_max -1)
        p_3 = self.spawn_rate[2]*probab**2
        p_2 = self.spawn_rate[1]*(2* probab - probab**2)
        p_1 =  1 - p_2 - p_3
        
        ran = random.random()
        print("------------------------------------------")
        print(f"wall: {p_1 *100:.1f}%\nnarrow: {p_2*100:.1f}%\ntri_wall: {p_3*100:.1f}%\n->random = {ran*100:.1f}%")
        
        if ran < p_1:
            return choose_obj[0]
        elif ran < p_1+p_2: 
            return choose_obj[1]
        else:
            return choose_obj[2]
        
        
    def score_collision_check(self,player):
        any_collision = any(Grect.colliderect(player) for Grect in self.__objs[0].score_rect_collision())

        if any_collision:
            if self.__is_hit == False:
                self.score += 1
                self.__is_hit = True
        else:
            self.__is_hit = False
    