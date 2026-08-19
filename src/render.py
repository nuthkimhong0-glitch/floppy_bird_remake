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
    
    _background = construct_background(assets)
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
        choice = background_choice(gameplay[0].score(),5)
        screen.blit(background(_background,choice),(0,-304)) # from total background size y minus screen y

        if not gameplay[0].is_new_game:
            gameplay[0].game_logic(game_start,new_game)
        else: 
            game_start = False
            new_game = False
            gameplay.pop(0)
            gameplay.append(game_play(screen))
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(global_variable.FPS)  # limits FPS to 60

    pygame.quit()
  
def construct_background(assets):
    background_days = [assets.images_based_line[0] for _ in range(5)]
    background_nights = [assets.images_based_line[1] for _ in range(5)]
    background_days_flip = [assets.images_based_line[0] for _ in range(5)]
    background_nights_flip = [assets.images_based_line[1] for _ in range(5)]
    
    for i in range(5):
        background_days_flip[i] = pygame.transform.flip(background_days_flip[i],False,True)
        background_nights_flip[i] = pygame.transform.flip(background_nights_flip[i],False,True)
    
    w,h = background_days[0].get_size()
    
    surface_days = pygame.Surface((w*5,h*2), pygame.SRCALPHA)
    surface_night = pygame.Surface((w*5,h*2), pygame.SRCALPHA)
    
    for i in range(5):
        surface_days.blit(background_days_flip[i],(w*i,0)) 
        surface_days.blit(background_days[i],(w*i,h)) 
        surface_night.blit(background_nights_flip[i],(w*i,0)) 
        surface_night.blit(background_nights[i],(w*i,h)) 
    
    return [surface_days,surface_night]
def background(surface_background, choose):
    match(choose):
        case 0:
            return surface_background[0]
        case 1:
            return surface_background[1]

#bruh why ts math work i have no idea
def background_choice(score, set_sequence):
    # Integer division (//) finds how many 'sequences' have passed.
    # Modulo 2 (% 2) ensures it always loops back to 0 or 1.
    return (score // set_sequence) % 2


class game_play:
    def __init__(self,screen):
        self.m = mechanic.Mbird(screen,assets)
        self.w = mechanic.MWall(screen,assets)
        self.ui_ = ui.score(screen)
        self.menu = ui.menu(screen)
        self.end = ui.lose(screen)
        
        self.is_game_start = False
        self.is_game_pause = True
        self.is_game_end = False
        self.is_new_game = False
        
        self.game_pause(True)
    
    def game_logic(self,register_game_start,register_new_game):
        
        self.w.update()
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