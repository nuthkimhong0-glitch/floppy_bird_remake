import pygame
import global_variable
from import_asset import game_asset

class background:
    def __init__(self,assets,background_cycle):
        self.__background = self.construct_background(assets,5)
        self.__cycle = background_cycle
    
    def background_relative_pos(self):
        return (0,-304)# from total background size y minus screen y
    def background_update(self,gameplay):
        choice = self.background_choice(gameplay.score(),self.__cycle)
        return self.background(self.__background ,choice) 
    
    def construct_background(self,assets,n):
        background_days = [assets.images_based_line[0] for _ in range(n)]
        background_nights = [assets.images_based_line[1] for _ in range(n)]
        background_days_flip = [assets.images_based_line[0] for _ in range(n)]
        background_nights_flip = [assets.images_based_line[1] for _ in range(n)]
        
        for i in range(n):
            background_days_flip[i] = pygame.transform.flip(background_days_flip[i],False,True)
            background_nights_flip[i] = pygame.transform.flip(background_nights_flip[i],False,True)
        
        w,h = background_days[0].get_size()
        
        surface_days = pygame.Surface((w*n,h*2), pygame.SRCALPHA)
        surface_night = pygame.Surface((w*n,h*2), pygame.SRCALPHA)
        
        for i in range(n):
            surface_days.blit(background_days_flip[i],(w*i,0)) 
            surface_days.blit(background_days[i],(w*i,h)) 
            surface_night.blit(background_nights_flip[i],(w*i,0)) 
            surface_night.blit(background_nights[i],(w*i,h)) 
        
        return [surface_days,surface_night]

    def background(self,surface_background, choose):
        match(choose):
            case 0:
                return surface_background[0]
            case 1:
                return surface_background[1]

    #bruh why ts math work i have no idea
    def background_choice(sefl,score, set_sequence):
        # Integer division (//) finds how many 'sequences' have passed.
        # Modulo 2 (% 2) ensures it always loops back to 0 or 1.
        return (score // set_sequence) % 2
    
class base_line:
    def __init__(self,assets):
        self.__pre_assets = assets.images_based_line[2]
        self.__baseline = self.__baselin_construct(assets,5)
    
    def relative_position(self,offeset):
        w,h = self.__pre_assets.get_size()
        
        lowwer_pos_y = global_variable.SCREEN_SIZE_Y - offeset
        upper_pos_y = -h + offeset
        
        return upper_pos_y,lowwer_pos_y
     
    def baseline_update(self):   
        return self.__baseline
        
    def __baselin_construct(self,assets,n):
        upper = [assets.images_based_line[2] for _ in range(n)]
        lowwer = [assets.images_based_line[2] for _ in range(n)]
        
        
        for i in range(n):
            upper[i] = pygame.transform.flip(upper[i],False,True)
        
        w,h = lowwer[0].get_size()
        
        surface_upper = pygame.Surface((w*n,h), pygame.SRCALPHA)
        surface_lowwer = pygame.Surface((w*n,h), pygame.SRCALPHA)
        
        for i in range(n):
            surface_upper.blit(upper[i],(w*i,0)) 
            surface_lowwer.blit(lowwer[i],(w*i,0)) 
        
        return [surface_upper,surface_lowwer]