import pygame
import global_variable
import mechanic
import ui

def render():
    pygame.init()
    screen = pygame.display.set_mode((global_variable.SCREEN_SIZE_X, global_variable.SCREEN_SIZE_Y))
    clock = pygame.time.Clock()
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
        self.m = mechanic.Mbird(screen)
        self.w = mechanic.MWall(screen)
        self.ui_ = ui.score(screen)
        self.menu = ui.menu(screen)
        self.end = ui.lose(screen)
        
        self.is_game_start = False
        self.is_game_pause = True
        self.is_game_end = False
        self.is_new_game = False
    
        self.game_start()
    
    def game_logic(self):
        
        self.w.update()
        self.m.update()
        
        
        if not self.is_game_start:
            self.menu.render_text()
            self.is_game_start = self.menu.input()
        else:
            self.is_game_pause = False
            self.game_start()
            self.collision_logic()
            if not self.is_game_end:
                self.ui_.update(self.w.score)
            else:
                self.end.update()
                self.end.score = self.w.score
                self.is_new_game = self.end.input()
        
    
    def game_start(self):
        for obj in self.w.objs:
            obj.is_game_pause = self.is_game_pause
        self.m.is_game_pause = self.is_game_pause
        
    def collision_logic(self):
        state = False
        #idk how to combine the system properly here, just do it right here for now i guess
        is_rect_hit = self.w.collision_check(self.m.collision())       
        is_triangle_hit = self.w.triangle_collision_check(self.m)
        self.w.score_collision_check(self.m.collision())
        
        if is_rect_hit or is_triangle_hit: 
            state = True
            
        #temporaly push game (idk what to do yet)
        if state :
            for obj in self.w.objs:
                obj.is_game_pause = True
            self.m.is_game_pause = True
            self.is_game_end = True