import pygame
import global_variable
import mechanic
import ui
from import_asset import game_asset

pygame.init()
screen = pygame.display.set_mode((global_variable.SCREEN_SIZE_X, global_variable.SCREEN_SIZE_Y))
assets = game_asset()
clock = pygame.time.Clock()

def render():
    running = True
    gameplay = []    
    [gameplay.append(game_play(screen)) for _ in range(2)]
    
    
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("yellow")

        if not gameplay[0].is_new_game:
            gameplay[0].game_logic()
        else: 
            gameplay.pop(0)
            gameplay.append(game_play(screen))
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(global_variable.FPS)  # limits FPS to 60

    pygame.quit()
  
            
        
class game_play:
    def __init__(self,screen):
        self.m = mechanic.Mbird(screen,assets)
        self.w = mechanic.MWall(screen)
        self.ui_ = ui.score(screen)
        self.menu = ui.menu(screen)
        self.end = ui.lose(screen)
        
        self.is_game_start = False
        self.is_game_pause = True
        self.is_game_end = False
        self.is_new_game = False
        
        self.__is_hold = False
        
        self.game_pause(True)
    
    def game_logic(self):
        
        self.w.update()
        self.m.update()
        
        
        if not self.is_game_start:
            self.menu.render_text()
            self.is_game_start = self.menu_input()
        else:
            self.game_pause(False)
            self.collision_logic()
            if not self.is_game_end:
                self.ui_.update(self.w.score)
            else:
                self.end.update()
                self.end.score = self.w.score
                self.is_new_game = self.menu_input()
                
    # there is a bug that if i press space fast it glicth into new game play and showing 
    # the text for a split the second then game play
    # i guess i call that a feature =D 
    def menu_input(self): 
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            if not self.__is_hold:
                self.__is_hold = True
                return True
        else:
            self.__is_hold = False
        return False
            
    
    def game_pause(self,isgamepause):
        for obj in self.w.objs:
            obj.is_game_pause = isgamepause
        self.m.is_game_pause = isgamepause
        
    def collision_logic(self):
        state = False
        
        is_rect_hit = self.w.collision_check(self.m.collision())       
        is_triangle_hit = self.w.triangle_collision_check(self.m)
        self.w.score_collision_check(self.m.collision())
        
        if is_rect_hit or is_triangle_hit: 
            state = True
            
        if state :
            self.game_pause(True)
            self.is_game_end = True