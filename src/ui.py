from mechanic import MWall
import pygame
import global_variable

class menu:
    def __init__(self,Screen,assets):
        self.__screen = Screen
        self.__assets = assets
        self.__image = self.__assets.image_customs[1]
        self.pX = global_variable.SCREEN_SIZE_X/2 - self.__image.get_width()/2
        self.pY = global_variable.SCREEN_SIZE_Y/2 - self.__image.get_height()/2
        
    def update(self):
        self.render_text()
        
    def render_text(self):
        game_font = pygame.font.Font(None,50)
        # text = game_font.render(str("Play!"), True, (0,0,0))
        self.__screen.blit(self.__image,(self.pX,self.pY))
        
class score:
    def __init__(self,Screen,assets):
        self.__screen = Screen
        self.score = 0
        self.__images = [assets.images_nums[i] for i in range(10)]
        self.__digits = [0]
        self.pX = global_variable.SCREEN_SIZE_X/2 - 12
        self.pY = 50
        self.tmp = 0
    def update(self,score):
        self.render_text(score)
        
    def render_text(self,score):
        #prevent using again and again from digits value
        if self.tmp != score:
            self.__digits = self.get_digits(score)
            self.tmp = score
            
        game_font = pygame.font.Font(None,50)
        text = game_font.render(str(score), True, (0,0,0))
        gap = 0
        for i in range(len(self.__digits)):
            if i!= 0: 
                gap += 24
            self.__screen.blit(self.show_num(self.__digits[i]),(self.pX + gap,self.pY))

    def get_digits(self,score):
        digits = []
        num = score
        if num == 0:
            digits.append(0)
        else:
            while num>0:
                last = num% 10
                digits.append(last)
                num = num // 10
                
            digits.reverse()
        # print(f'{digits}')
            
        return digits
        
    def show_num(self,get_digits):
        return self.__images[get_digits]
        
class lose:
    def __init__(self,Screen,assets):
        self.__screen = Screen
        self.__assets = assets
        self.__images_num = [self.__assets.images_nums[i] for i in range(10)]
        self.__get_num = []
        self.__images = []
        self.__images.append(self.__assets.image_customs[0])
        self.__images.append(self.__assets.image_customs[2])
        self.score = 0
        self.pX = global_variable.SCREEN_SIZE_X/2 
        self.pY = global_variable.SCREEN_SIZE_Y/2
        self.__shifting =  self.__images[0].get_width()/2
        self.__one_time = 0
    def update(self):
        self.render_text()
        
    def render_text(self):
        game_font = pygame.font.Font(None,50)
        # text = game_font.render(str(f"Your Score: {self.score}"), True, (0,0,0))
        self.__screen.blit(self.__images[0],(self.pX- self.__shifting,self.pY - 50))
        self.__screen.blit(self.__images[1],(self.pX-(50+self.__shifting),self.pY))
        # idk why, but this is to update the score cuz the first time it the score stay 0, 
        # only the method update twice, thus it can show 
        if self.__one_time !=2 : 
            self.__get_num = self.get_digits(self.score)
            self.__one_time +=1 
            
        self.render_num()
        
    
    def render_num(self):
        # print(f'{self.__get_num}')
        gap = 0
        for i in range(len(self.__get_num)):
            if i!= 0: 
                gap += 24
            self.__screen.blit(self.__images_num[self.__get_num[i]],(self.pX + gap,self.pY+10))
            
            
    def get_digits(self,score):
        digits = []
        num = score
        if num == 0:
            digits.append(0)
        else:
            while num>0:
                last = num% 10
                digits.append(last)
                num = num // 10
                
            digits.reverse()
        return digits