import pygame
import os
import math
import random
from vector2D import Vector2
from physics import Distance,rad


class panel(object):
   '''
   Implements the Orb object
   '''

   def __init__(self,path,secondpath,xposition,yposition):
      '''
      initializes the Orb oject
      '''
    
      #initialize variables
      
      self.image= pygame.image.load(path).convert()
      self.reserveimage = pygame.image.load(path).convert()
      self.position = Vector2(0,0)
      self.position.x = xposition
      self.position.y = yposition
      self.dead = False
      
      if secondpath is not None:
         
          self.secondimage = pygame.image.load(secondpath).convert()
      else:
          self.secondimage = None
     
      
     
      
    
   
  
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
   def draw(self,surface, prereq = True,selected =False):
      '''
       Draws the orb
      '''
      self.image.set_colorkey(self.image.get_at((0,0)))
      
      
      if self.dead == False and prereq ==True:

         
         
         #self.image.set_colorkey(self.image.get_at((0,0)))
         surface.blit(self.image, list(self.position))

         if selected and self.secondimage is not None:
             #self.image.set_colorkey(self.secondimage.get_at((0,0)))
             
             surface.blit(self.secondimage, list(self.position))
         
             
             

 
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
      newRect =  self.position + self.image.get_rect()
      return newRect


   def getgatherspot(self):
       return self.spot
       
  

       


   def kill(self):
      self.dead  =True
   def isDead(self):
      return self.dead
        
