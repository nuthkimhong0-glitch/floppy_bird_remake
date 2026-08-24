from pathlib import Path
import pygame


class game_asset:
    def __init__(self):
        self.images_nums =[]
        self.images_based_line = []
        self.images_player =[]
        self.image_walls = []
        self.image_customs = []
        self.__load_all_asset()
        self.__load_custom_asset()
        
        
    def __load_all_asset(self):
        path = 'flappy-bird-assets-master/sprites'
        folder = Path(path)
        files = [f.name for f in folder.iterdir() if f.is_file()]
        files = [path +'/'+ f for f in files]    
        
        for i in range (len(files)):
            if i < 10:
                self.images_nums.append(pygame.image.load(files[i]).convert_alpha())
            else:
                if "background" in files[i] or "base" in files[i]:
                    self.images_based_line.append(pygame.image.load(files[i]).convert_alpha())
                elif "bluebird" in files[i]:
                    self.images_player.append(pygame.image.load(files[i]).convert_alpha()) 
                elif "pipe" in files [i]:
                    self.image_walls.append(pygame.image.load(files[i]).convert_alpha())
    
    def __load_custom_asset(self):
        path = 'custom_assets'
        folder = Path(path)
        files = [f.name for f in folder.iterdir() if f.is_file()]
        files = [path +'/'+ f for f in files]    
        for i in range (len(files)):
            if ".png" in files[i]:
                # print(f'{files[i]}')
                self.image_customs.append(pygame.image.load(files[i]).convert_alpha())
                
        # print(f'{self.image_customs.}')
        