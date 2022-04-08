
from doctest import ELLIPSIS_MARKER
import pygame
import os
import math
import random
from vector2D import Vector2
from physics import Distance,rad
from character import Character
class Dummy(Character):

    def __init___(self,path,xposition,yposition):
        self.walking = False
        self.imageres = self.image
        self.starttime =1
        self.dead= False
        self.HP = 100
        super().__init__(path,xposition,yposition)
    def shoot(self,clock,projectilelst,enemylst,framerate = 5):
        return None
   
    def walk(self,clock,framerate = 7):

        return None

    

    
    

        
        