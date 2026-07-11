import pygame

class bird_body:
    
    def __init__(self,screen):
        self.screen = screen
    
    def render(self,pX,vY,sX,sY):
        pygame.draw.rect(self.screen,(255,0,0),(pX,vY,sX,sY))
    
    # def collision(self):
        
