import pygame
import global_variable
import mechanic
import ui
import enviroment 
from import_asset import game_asset

pygame.init()
screen = pygame.display.set_mode((global_variable.SCREEN_SIZE_X, global_variable.SCREEN_SIZE_Y))
assets = game_asset()
clock = pygame.time.Clock()

def render():
    running = True
    gameplay = []    
    [gameplay.append(game_play(screen)) for _ in range(2)]
    background = enviroment.background(assets,10)
    baseline = enviroment.base_line(assets)
    game_start = False
    new_game = False
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_start = True
                    if gameplay[0].is_game_end:
                        new_game = True

        # fill the screen with a color to wipe away anything from last frame
        # screen.fill("yellow")
        
        _baseline = baseline.baseline_update()
        bs_upper,bs_lowwer = baseline.relative_position(10)
        screen.blit(background.background_update(gameplay[0]),background.background_relative_pos()) 

        if not gameplay[0].is_new_game:
            gameplay[0].game_logic(_baseline,[bs_upper,bs_lowwer],game_start,new_game)
        else: 
            game_start = False
            new_game = False
            gameplay.pop(0)
            gameplay.append(game_play(screen))
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(global_variable.FPS)  # limits FPS to 60

    pygame.quit()
  



class game_play:
    def __init__(self,screen):
        self.screen = screen
        self.m = mechanic.Mbird(screen,assets)
        self.w = mechanic.MWall(screen,assets)
        self.ui_ = ui.score(screen,assets)
        self.menu = ui.menu(screen,assets)
        self.end = ui.lose(screen,assets)
        
        
        self.is_game_start = False
        self.is_game_pause = True
        self.is_game_end = False
        self.is_new_game = False
        
        self.game_pause(True)
    
    def game_logic(self,baseline,base_pos,register_game_start,register_new_game):
        
        self.w.update()
        
        self.screen.blit(baseline[0],(0,base_pos[0]))
        self.screen.blit(baseline[1],(0,base_pos[1])) 
        
        self.m.update()
        
        
        if not self.is_game_start:
            self.menu.render_text()
            self.is_game_start = register_game_start
        else:
            self.game_pause(False)
            self.collision_logic()
            if not self.is_game_end:
                self.ui_.update(self.score())
            else:
                self.end.update()
                self.end.score = self.score()
                self.is_new_game = register_new_game
                
    def game_pause(self,isgamepause):
        for obj in self.w.objs:
            obj.is_game_pause = isgamepause
        self.m.is_game_pause = isgamepause
        
    def collision_logic(self):
        state = False
        
        is_rect_hit = self.w.collision_check(self.m.get_collision())       
        is_triangle_hit = self.w.triangle_collision_check(self.m)
        self.w.score_collision_check(self.m.get_collision())
        
        if is_rect_hit or is_triangle_hit: 
            state = True
            
        if state :
            self.game_pause(True)
            self.is_game_end = True
            
    def score(self):
        return self.w.score