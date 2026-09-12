import pygame
import global_variable
class bird_body:
    
    def __init__(self,Screen,assets,audio):
        self.screen = Screen
        self.player_asset = assets
        self.player_audio = audio.sounds_effect[4]
        self.hit_ground_audio = audio.sounds_effect[1]
        self,self.hit_ground_audio.set_volume(0.1)
        self.player_audio.set_volume(0.1)
        self.__chhanel_player = pygame.mixer.Channel(0)
        self.is_game_pause = False
        self.__pX = global_variable.SCREEN_SIZE_X - (global_variable.SCREEN_SIZE_X * (1-0.15))
        self.__py= global_variable.SCREEN_SIZE_Y/2
        self.__sizeX = 20
        self.__sizeY = 20
        
        self.__gravity = 0.1
        self.__jump_force = 2
        self.__v_y = 0
        
        self.__animatino_state = 0 # maximun 3 cuz have 3 frame of animation

        self.__is_hit_top_or_bottom_floor = False

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
                # self.__chhanel_player.play(self.player_audio)
                self.__is_held = False
        else:
            self.__is_held = True

        self.__v_y += self.__gravity
        self.__py += self.__v_y
        
        self.__fly_state = 0 #fly nomral, down, up
            
    
    def boundery(self):
        # the 10 offset for make the collision abit right with the size
        if self.__py < 0:
            self.__py = 0
            self.__v_y = 0
            if not self.__is_hit_top_or_bottom_floor:
                self.__chhanel_player.play(self.hit_ground_audio)
                self.__is_hit_top_or_bottom_floor = True
        elif self.__sizeY + self.__py+ 10> global_variable.SCREEN_SIZE_Y:
            self.__py = global_variable.SCREEN_SIZE_Y-self.__sizeY-10
            self.__v_y = 0
            if not self.__is_hit_top_or_bottom_floor:
                self.__chhanel_player.play(self.hit_ground_audio)
                self.__is_hit_top_or_bottom_floor = True
        else:
            self.__is_hit_top_or_bottom_floor = False
   
    def render(self):
        self.__animation()
        # pygame.draw.rect(self.screen,(255,0,0),self.get_rect_collision_point())
        bird = self.__sprite_rotation()
        self.screen.blit(bird,self.image_pos_bird())
        
    def image_pos_bird(self):
        rect = pygame.Rect(self.__pX,self.__py,self.__sizeX,self.__sizeY)
        return rect
    
    def get_rect_collision_point(self):
        if self.__fly_state == 0:
            self.__rect = pygame.Rect(self.__pX+10,self.__py,self.__sizeX,self.__sizeY)
        elif self.__fly_state == 1:
            self.__rect = pygame.Rect(self.__pX+10,self.__py+10,self.__sizeX,self.__sizeY)
        elif self.__fly_state == 2:
            self.__rect = pygame.Rect(self.__pX+10,self.__py+10,self.__sizeX,self.__sizeY)
        return self.__rect
    
    def __sprite_rotation(self,buff_zone = 1):
        speed = self.__v_y
        speed = int(speed)
        bird = self.player_asset.images_player[int(self.__animatino_state)]
        if speed >-buff_zone and speed < buff_zone:
            self.__fly_state = 0
            bird = pygame.transform.rotate(bird,0)
        elif speed < -buff_zone:
            self.__fly_state = 1
            bird = pygame.transform.rotate(bird,25)
        elif speed > buff_zone:
            self.__fly_state = 2
            bird = pygame.transform.rotate(bird,-25)
            
        return bird
    
    def __animation(self):
        if self.__animatino_state < 2.9: 
            self.__animatino_state += global_variable.GLOBAL_ANIMATION_SPEED
        else:
            self.__animatino_state = 0