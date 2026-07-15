import pygame
import global_variable
import mechanic

def render():
    pygame.init()
    screen = pygame.display.set_mode((global_variable.SCREEN_SIZE_X, global_variable.SCREEN_SIZE_Y))
    clock = pygame.time.Clock()
    running = True
    
    m = mechanic.Mbird(screen)
    w = mechanic.MWall(screen)
    
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("yellow")

        w.update()
        m.update()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(global_variable.FPS)  # limits FPS to 60

    pygame.quit()
    
