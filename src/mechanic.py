import global_variable
import random
import walls
import math
from bird import bird_body
import pygame

class Mbird: # Mehcanic bird    
    def __init__(self,Screen,assets):
        self.screen = Screen
        self.b = bird_body(Screen,assets)
        self.is_game_pause = False
    
    def update(self):
        self.b.update()
        self.b.is_game_pause = self.is_game_pause
    def collision (self):
        return self.b.rect_collision_point()
    ## ai =D
    def check_collision(self, wall_object):
        """
        Checks pixel-perfect collision against a narrow_wall or triangle_wall instance.
        Returns True if colliding, False otherwise.
        """
        bird_mask, (bird_x, bird_y) = self.b.get_mask_data()
        
        # Iterate over all masks returned by the wall's get_masks() method
        for wall_mask, (wall_x, wall_y) in wall_object.get_masks():
            # Offset is wall position relative to bird position
            offset = (int(wall_x - bird_x), int(wall_y - bird_y))
            
            if bird_mask.overlap(wall_mask, offset):
                return True
                
        return False
    ## end here
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
        self.__tri_wall = [walls.triangle_wall(self.screen,10) for _ in range(self.num_of_wall_2[0])]
        self.__rect_score_point = [] #G for goal?? idk what is the right name
        
        self.__rect_walls_lists = []
        
        self.last_pos = 0
        self.order = order
        
        self.is_game_pause = False
        
    def spawn(self):
        currentX = global_variable.SCREEN_SIZE_X
        self.__lead.pX = currentX
        
        match self.order:
            case 0:
                for  i  in range(self.num_of_wall_1[0]):
                    self.__wallp[i].pX = currentX
                    self.__wallp[i].upper_rect.x = currentX
                    self.__wallp[i].lowwer_rect.x = currentX
                    self.__rect_walls_lists.append(self.__wallp[i].upper_rect)
                    self.__rect_walls_lists.append(self.__wallp[i].lowwer_rect)
                    self.__rect_score_point.append(pygame.Rect(self.__wallp[i].pX+self.__wallp[i].sizeX-5,0,5,720))
                    
                    currentX += global_variable.GLOBAL_SHIFT_POSITION_X_FROM_EACH_OTHER + self.__wallp[i].sizeX
            case 1:
                self.__narrow_wall.pX = currentX
                self.__narrow_wall.upper_rect.x = currentX
                self.__narrow_wall.lowwer_rect.x = currentX
                self.__rect_walls_lists.append(self.__narrow_wall.upper_rect)
                self.__rect_walls_lists.append(self.__narrow_wall.lowwer_rect)
                self.__rect_score_point.append(pygame.Rect(self.__narrow_wall.pX+self.__narrow_wall.sizeX-5,0,5,720))
                currentX += global_variable.GLOBAL_SHIFT_POSITION_X_FROM_EACH_OTHER + self.__narrow_wall.sizeX
            case 2:
                size_px = self.__tri_wall[0].size_x
                for i in range(self.num_of_wall_2[0]):
                    self.__tri_wall[i].poX = [x+currentX for x in self.__tri_wall[i].poX]
                    self.__tri_wall[i].poX_shift = [x+currentX for x in self.__tri_wall[i].poX_shift]
                    self.__tri_wall[i].set_pos()
                    currentX += size_px
                self.__rect_score_point.append(pygame.Rect(self.__tri_wall[-1].poX_shift[1],0,5,720))
                currentX += global_variable.GLOBAL_SHIFT_POSITION_X_FROM_EACH_OTHER + self.__tri_wall[0].offSetX

        self.last_pos = currentX - self.__tri_wall[0].offSetX *0
    
    def __which_to_spawn(self):
        if self.order == 0 :
            for w1 in self.__wallp[:]:
                w1.update()
                w1.is_game_pause = self.is_game_pause
        elif self.order == 1:
            self.__narrow_wall.update()
            self.__narrow_wall.is_game_pause = self.is_game_pause
        elif self.order == 2:
            for t1 in self.__tri_wall[:]:
                t1.update()
                t1.is_game_pause = self.is_game_pause
            
    def get_triangle_walls(self):
        # Only return the triangle walls if this Object spawned them (order 2)
        if self.order == 2:
            return self.__tri_wall
        return []
    def update(self):
        
        self.__which_to_spawn()
            
        if not self.is_game_pause:
            for rect in self.__rect_score_point:
                # pygame.draw.rect(self.screen,(0,24,233),rect)
                rect.x -= global_variable.GLOBAL_SPEED_X
            for rect in self.__rect_walls_lists:
                rect.x -= global_variable.GLOBAL_SPEED_X
            self.last_pos -= global_variable.GLOBAL_SPEED_X
            # self.__lead.update()
        
    def rect_walls_collision(self):
        return self.__rect_walls_lists
    
    def score_rect_collision(self):
        return self.__rect_score_point     
class MWall:
    def __init__(self,Screen):
        self.screen = Screen
            
        self.score =0
        self.level_max = 5
        self.spawn_rate = global_variable.GLOBAL_SPAWN_RATE
        self.growth_rate = global_variable.GLOBAL_GROWTH_RATE
        # self.__half_step = int(math.log(self.level_max)/self.growth_rate)

        self.num_of_spawn = 5
        self.objs = []
        self.__is_hit = False
        first_obj = Object(self.screen,self.num_of_spawn,self.choose_algorithm())
        first_obj.spawn()
        self.objs.append(first_obj)
        
    def update(self):
        self.spawn_mechanics()
        
    def spawn_mechanics(self):
        
        for obj in self.objs:
            obj.update()
        
        if self.objs[-1].last_pos < global_variable.SCREEN_SIZE_X:
            new_obj = Object(self.screen, self.num_of_spawn, self.choose_algorithm())
            new_obj.spawn()
            self.objs.append(new_obj)
            
        if self.objs[0].last_pos < -10:
            self.objs.pop(0)
                
                
        
    def choose_algorithm(self):
        #i ask the ai then i got this formula, i impliment them cool
        choose_obj = [0,1,2]
        current_level = self.level_max/(1+(self.level_max-1)*math.pow(math.e,-self.growth_rate*self.score))
        
        probab = (current_level - 1)/ (self.level_max -1)
        p_3 = self.spawn_rate[2]*probab**2
        p_2 = self.spawn_rate[1]*(2* probab - probab**2)
        p_1 =  1 - p_2 - p_3
        
        ran = random.random()
        # print("------------------------------------------")
        # print(f"wall: {p_1 *100:.1f}%\nnarrow: {p_2*100:.1f}%\ntri_wall: {p_3*100:.1f}%\n->random = {ran*100:.1f}%")
        
        if ran < p_1:
            return choose_obj[0]
        elif ran < p_1+p_2: 
            return choose_obj[1]
        else:
            return choose_obj[2]
        
    def collision_check(self,player):
        for obj in self.objs:
            for rect in obj.rect_walls_collision():
                if rect.colliderect(player):
                    return True
    #ai here
    def triangle_collision_check(self, player_mbird):
        """Checks mask collisions ONLY for triangle_wall objects."""
        bird_mask, (bird_x, bird_y) = player_mbird.b.get_mask_data()

        # Loop through the Object containers first
        for obj in self.objs:
            # Grab the actual triangle walls from inside the Object
            for wall in obj.get_triangle_walls():
                
                # Now we can safely get masks and check overlap
                for wall_mask, (wall_x, wall_y) in wall.get_masks():
                    offset = (int(wall_x - bird_x), int(wall_y - bird_y))
                    if bird_mask.overlap(wall_mask, offset):
                        return True

        return False
    #end here
    def score_collision_check(self,player):
        any_collision = any(score_rect.colliderect(player) for score_rect in self.objs[0].score_rect_collision())

        if any_collision:
            if self.__is_hit == False:
                self.score += 1
                self.__is_hit = True
        else:
            self.__is_hit = False
    