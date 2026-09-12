from pathlib import Path
import pygame
import compile
import sys
import os

#ai here
# Get PyInstaller's hidden temp directory, or fall back to normal directory
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    BASE_PATH = Path(sys._MEIPASS)
else:
    BASE_PATH = Path(".")
#end here
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
        # path = 'flappy-bird-assets-master/sprites'
        # folder = Path(path)
        # files = [f.name for f in folder.iterdir() if f.is_file()]
        # files = [path +'/'+ f for f in files]    
        
        #that ai code for compile 
        # When compiled, the folder is just called 'sprites'
        folder_name = 'sprites' if getattr(sys, 'frozen', False) else 'flappy-bird-assets-master/sprites'
        folder = BASE_PATH / folder_name
        
        # Gather file paths cleanly using pathlib
        files = [str(f) for f in folder.iterdir() if f.is_file()]
        #end here
        for i in range (len(files)):
            if i < 10:
                self.images_nums.append(pygame.image.load(compile.resource_path((files[i]))).convert_alpha())
            else:
                if "background" in files[i] or "base" in files[i]:
                    self.images_based_line.append(pygame.image.load(compile.resource_path((files[i]))).convert_alpha())
                elif "bluebird" in files[i]:
                    self.images_player.append(pygame.image.load(compile.resource_path(files[i])).convert_alpha()) 
                elif "pipe" in files [i]:
                    self.image_walls.append(pygame.image.load(compile.resource_path(files[i])).convert_alpha())
    
    def __load_custom_asset(self):
        # path = 'custom_assets'
        # folder = Path(path)
        # files = [f.name for f in folder.iterdir() if f.is_file()]
        # files = [path +'/'+ f for f in files]    
        
        #ai
        folder = BASE_PATH / 'custom_assets'
        files = [str(f) for f in folder.iterdir() if f.is_file()]
        #end
        
        for i in range (len(files)):
            if ".png" in files[i]:
                # print(f'{files[i]}')
                self.image_customs.append(pygame.image.load(compile.resource_path(files[i])).convert_alpha())
                
        # print(f'{self.image_customs.}')

class audio_game_assets:
    def __init__(self):
        self.sounds_effect = []
        self.load_audio()
    
    def load_audio(self):
        # path = 'flappy-bird-assets-master/audio'
        # folder = Path(path)
        # files = [f.name for f in folder.iterdir() if f.is_file()]
        # files = [path +'/'+ f for f in files]
        
        #ai
        # When compiled, the folder is just called 'audio'
        folder_name = 'audio' if getattr(sys, 'frozen', False) else 'flappy-bird-assets-master/audio'
        folder = BASE_PATH / folder_name
        
        files = [str(f) for f in folder.iterdir() if f.is_file()]
        #end
            
        n=0
        for i in range(len(files)):
            if ".wav" in files[i]:
                # print(f'N: {n}: {files[i]}')
                self.sounds_effect.append(pygame.mixer.Sound(compile.resource_path(files[i])))
                n+=1