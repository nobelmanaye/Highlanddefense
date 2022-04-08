import pygame
import os
import math
import random
from vector2D import Vector2
from physics import Distance,rad
from drawable import drawable

class resource(drawable):
   '''
   Implements the Orb object
   '''

   def __init__(self,path,xposition,yposition,spotlst,kind):
      '''
      initializes the Orb oject
      '''
      self.kind = kind
      #initialize variables
      super().__init__(path,xposition,yposition)
      self.image= pygame.image.load(path).convert()
      self.velocity = Vector2(0,0)
      self.position = Vector2(0,0)
      self.position.x = xposition
      self.position.y = yposition
      self.dead = False
      self.spots = spotlst
      
     
      self.gathererlst = [0 for x in range(len(self.spots))]
      newspotlst = []
      for spots in self.spots:
         oldx = spots[0]
         oldy = spots[1]
         spots = (self.position.x + oldx,self.position.y +oldy)
         newspotlst.append(spots)
      self.spots = newspotlst
        
      #self.spots = [-28 + self.position.x,-18+self.position.y, ]
      self.occupied = False

  
  
   def draw(self,surface):
      '''
       Draws the orb
      '''
      
      
      if self.dead == False:
         
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))


   def selected(self):
       self.selected = True
       #self.image = slightly beiged image

   def Isoccupied(self):
      return self.occupied
   def getgatherspot(self):
       for item in self.gathererlst:
          if item == 0:
             return self.gathererlst.index(item)
       
       
   def markandgogather(self,miner):
      print(" this is self.spots" + str(self.spots))
      markeditem =0
      copygatherer =self.gathererlst.copy()
      #print("This is self.spots" + str(self.spots))
      #print("This is self.gatherer" + str(self.gathererlst))
      if 0 not in self.gathererlst:
         self.occupy()
      elif 0 in self.gathererlst:
         self.unoccupy()
      for item in copygatherer:
          if item == 0:
             markeditem = copygatherer.index(item)
             #print(" This is what I am returned" + str(self.spots[self.gathererlst.index(item)]))
             self.gathererlst[markeditem] = 1
             if 0 not in self.gathererlst:
                self.occupied = True
             miner.beginmoving(self.spots[copygatherer.index(item)])
             return 
      
   
   def unmark(self,position):
      
      self.gathererlst[position] = 0
      #print(" making this zero " + str(position) + " here is list " + str(self.gathererlst))
      if 0 not in self.gathererlst:
         self.occupy()
      elif 0 in self.gathererlst:
         self.unoccupy()
   def occupy(self):
      self.occupied = True
   
   def unoccupy(self):
      self.occupied = False
      

      
      
      
       
       

       
  

