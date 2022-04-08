
import pygame
import os

class resourceregister(object):
    def __init__(self):
        self.gold = 0
        self.wood = 0
        self.food = 0
        
        self.image = pygame.image.load(os.path.join("images","goldingot.PNG")).convert()
    def addFood(self,foodamount):
        self.food+= foodamount
    
    def addGold(self,goldamount):
        self.gold += goldamount
    def addWood(self,woodamount):
        self.wood += woodamount
    def getgoldstring(self):
        return str(self.gold)
    def draw(self,surface):
        surface.blit(self.image, (828,794))
        self.image.set_colorkey(self.image.get_at((0,0)))

        text = pygame.font.SysFont("Arial",16)

        
        Gold = text.render( (  str(self.gold)),False,(0,0,0) )

        Wood = text.render( (str(self.wood)),False,(0,0,0) )
        
        surface.blit(Gold,(894,800))

        surface.blit(Wood,(980,800))
    def existsenough(self, wood,gold):
        
        return (self.wood >= wood and self.gold >= gold)
        
        
        goldcount = text.render(str(round(self.gold)), False, (0,0,0))
        surface.blit(goldcount, (886,810))

                
        woodcount = text.render(str(round(self.wood)), False, (0,0,0))
        surface.blit(woodcount, (930,810))
        