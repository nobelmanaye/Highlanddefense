import pygame
import os
import math
import random
from vector2D import Vector2
from physics import Distance,rad


class drawable(object):
   '''
   Implements the Orb object
   '''

   def __init__(self,path,xposition,yposition):
      '''
      initializes the Orb oject
      '''

      #initialize variables
      
      self.image= pygame.image.load(path).convert()
      
      self.velocity = Vector2(0,0)
      self.position = Vector2(0,0)
      self.position.x = xposition
      self.position.y = yposition
      self.selimage = self.image
      self.imageres = self.image
     
      #generate starting conditions for the orb(including random desired speeds, velocity & position vecs)
      
      
   
  
   def getPosition(self):
      '''
      Returns the positional vector of the orb
      '''
      return self.position
   def getX(self):

      return self.position.x

   def getY(self):
      return self.position.y

   def getWidth(self):
      '''
      Returns the width of the orb image
      '''
      return self.image.get_width()
  

   def getHeight(self):
      '''
      Returns the height of the orb
      '''
      return self.image.get_height()
   def draw(self,surface):
      '''
       Draws
      '''
      surface.blit(self.image, list(self.position))
      self.image.set_colorkey(self.image.get_at((0,0)))
         

 
   def getSize(self):
      '''
      Returns the size of the orb
      '''
      return self.image.get_size()

   
  
      
      
         

   def getOffset(self):
      '''
         returns a Vector2 variable containing the offset for drawing things to the screen.
      '''
      return Vector2(max(0,
                        min(self.position.x + (self.image.get_width() // 2) - \
                            (SCREEN_SIZE[0] // 2),
                            WORLD_SIZE[0] - SCREEN_SIZE[0])),
                    max(0,
                        min(self.position.y + (self.image.get_height()// 2) - \
                            (SCREEN_SIZE[1] // 2),
                            WORLD_SIZE[1] - SCREEN_SIZE[1])))

   def getCollisionRect(self):
      oldrect = self.image.get_rect()
      modified = oldrect.inflate(-0.3,-0.3)
      newRect =  self.position + modified 
      return newRect

