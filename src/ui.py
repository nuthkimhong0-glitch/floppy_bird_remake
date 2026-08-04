from mechanic import MWall
import pygame
import global_variable

class score:
    def __init__(self,Screen):
        self.__screen = Screen
        self.score = 0
        self.pX = global_variable.SCREEN_SIZE_X/2
        self.pY = 50
        
    def update(self,score):
        self.render_text(score)
        
    def render_text(self,score):
        game_font = pygame.font.Font(None,50)
        text = game_font.render(str(score), True, (0,0,0))
        self.__screen.blit(text,(self.pX,self.pY))
