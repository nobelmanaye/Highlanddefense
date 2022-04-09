'''
Nobel Manayhe

Implements an automatcially moving orb that is followed by a camera

'''

import pygame
import os
import math
import random
from vector2D import Vector2
from physics import Distance,rad
from testgraph import astar
from drawable import drawable
from character import Character
# Two different sizes now! Screen size is the amount we show the player,
#  and world size is the size of the interactable world
SCREEN_SIZE = Vector2(800, 800)
WORLD_SIZE = Vector2(1200, 900)



class Citizen(Character):
   '''
   Implements the Orb object
   '''

   def __init__(self,xposition,yposition):
      '''
      initializes the Orb oject
      '''

      #initialize variables
      path = os.path.join("images","citizen2.png")
      super().__init__(path,xposition,yposition)

      #reserve image to be looked on incase self.image changes due to events
      self.imageres = pygame.image.load(os.path.join("images\walking","180walking1.png")).convert()
      self.image= pygame.image.load(os.path.join("images\walking","180walking1.png")).convert()
      self.selimage = pygame.image.load(os.path.join("images\walking","selected.png"))
      self.buildimage = None
      self.dead = False
      
      self.mineimage = self.image
      self.keepdistance = 10
      #generate starting conditions for the orb(including random desired speeds, velocity & position vecs)
      self.chopimage = None
      self.miningrate = 0.07
      self.choppingrate = 0.07
      self.buildrate = 3
      self.mining = False
      self.building = False
      self.targetbuild = None
      self.minepos = None
      self.choppos = None
      self.targetmine = None
      self.targettree = None
      self.buildspot= None
      self.minesound = pygame.mixer.Sound(os.path.join("sound","mining.wav"))
      self.chopsound = pygame.mixer.Sound(os.path.join("sound","chopping.wav"))
      #self.buildsound = pygame.mixer.Sound(os.path.join("sound","building.wav"))
      self.citizenlst = []
      self.walkcursor =1
      self.minecursor =1
      self.buildcursor =1
      self.minestart =5
      #self.graph.mark(self.getHeight(), self.getWidth(), list(self.position))
      self.starttime =1
      self.chopping = False
      self.chopcursor =1
      self.cost = [0,10]


   


   def goMine(self,mine):
      '''
      Changes state to mining      
      '''
      self.minepos = mine.getgatherspot()
      self.mining = True
      self.targetmine = mine
   def goChop(self,tree):
      '''
      Changes state to mining      
      '''
      self.targettree = tree
      self.choppos = tree.getgatherspot()
      self.chopping = True
      
   def gobuild(self,building):
      self.building = True
     
      self.mining = False
      self.chopping = False
      self.struct = building
      

   def changetime(self,time):
      '''
      Resets the time cursor used for animation
      '''
      self.starttime = time
      
   def changeminetime(self,time):
      '''
      Resets the time cursor used for walking
      '''
      self.minestart = time
 
   def draw(self,surface):
      '''
       Draws the citizen
      '''    
      #pygame.draw.rect(surface,(0,0,255),self.getCollisionRect())  
      for item in self.sensorls:
         item.draw(surface)

      #rint("1  X Velocity : "+ str(round(self.velocity.x)) + " Y  Velocity" + str(round(self.velocity.y)))
      #print("   x direction : "+ str(round(self.position.x)) + " Y direction" + str(round(self.position.y)))
      
      if [self.dead,self.mining,self.going,self.chopping,self.building] == [False,False,False,False,False]:
      #its in a nothing state here, doing nothing
         self.image= self.imageres
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))
         
      
      if self.selected ==True:
         #It is selected
         
         surface.blit(self.selectedim,[self.getPosition().x+1,self.getPosition().y-25])
         self.selectedim.set_colorkey(self.selectedim.get_at((0,0)))
         
    
         #surface.blit(self.image, list(self.position))
         #self.image.set_colorkey(self.image.get_at((0,0)))
      if self.going ==True:
         #If its going, blit the ewalking image. 
         self.image = self.walkimage
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))
      
      if self.mining ==True and self.arrived ==True:
         surface.blit(self.mineimage, list(self.position))
         self.mineimage.set_colorkey(self.mineimage.get_at((0,0)))
      elif self.chopping ==True and self.arrived ==True and self.chopimage is not None:
         surface.blit(self.chopimage, list(self.position))
         self.chopimage.set_colorkey(self.mineimage.get_at((0,0)))
      elif self.building ==True and self.arrived ==True and self.buildimage is not None:
         surface.blit(self.buildimage, list(self.position))
         self.buildimage.set_colorkey(self.buildimage.get_at((0,0)))
      
      

   def chop(self,clock,wood):
      '''
      Makes the citizen mine

      '''
     
      frame = 6
      time = clock.get_ticks()/100
      if self.chopping == True and self.arrived ==True:
           
        
            if (abs(self.starttime-time)> 2):
               self.changeminetime(time) 
              
        
                     
               
               # Draw the mining citizen ( Drawing it here instead of Draw method because of increased clarity)
               self.chopimage = pygame.image.load(os.path.join("images\chopping","chopping"+str(max(1,round(self.chopcursor/frame)))+".png")).convert()
               self.chopimage.set_colorkey(self.image.get_at((0,0)))
               #surface.blit(self.image, list(self.position))
               #self.image.set_colorkey(self.image.get_at((0,0)))
               
               # There are 9 animation frames with a wait time of 6 frames, so whenever the frame cursor is above 54, it recurses back to one
               if self.chopcursor <=8*frame:
                  self.chopcursor +=1
               
               
               if self.chopcursor >8*frame:
                  self.chopcursor = 1
               if self.chopcursor ==6*frame:
                  wood += self.choppingrate
                  self.chopsound.play()
          
      else:
         
         # Set it to the reserve image
         self.image = self.imageres
         self.mining ==False

   def mine(self,clock,gold):
      '''
      Makes the citizen mine
      '''
      
      frame = 6

      time = clock.get_ticks()/100
      if self.mining == True and self.arrived ==True:
           
        
            if (abs(self.starttime-time)> 2):
               self.changeminetime(time) 
               # Draw the mining citizen ( Drawing it here instead of Draw method because of increased clarity)
               self.mineimage = pygame.image.load(os.path.join("images","axe"+str(max(1,round(self.minecursor/frame)))+".png")).convert()
               self.mineimage.set_colorkey(self.image.get_at((0,0)))
               #surface.blit(self.image, list(self.position))
               #self.image.set_colorkey(self.image.get_at((0,0)))
               
               # There are 9 animation frames with a wait time of 6 frames, so whenever the frame cursor is above 54, it recurses back to one
               if self.minecursor <=9*frame:
                  self.minecursor +=1
               if self.minecursor >9*frame:
                  self.minecursor = 1
               if self.minecursor ==4*frame:

                  gold += self.miningrate
                  self.minesound.play()
          
      else:
         
         # Set it to the reserve image
         self.image = self.imageres
         self.mining ==False
      
   def walk(self,clock,framerate = 7):
      ''''
      Walks the citizen as per the requested frame rate      
      '''
      
      frame =framerate

      #Weird time, but trial and error shows 28 is best for walking
      time = clock.get_ticks()/28

      #print("this is time: " + str(time) + " starttime : " + str(self.starttime)) 
      if self.going ==True:        

            direction = self.getAnglestate()
            if self.getAnglestate() not in ("270","180","90","0"):
               direction = "0"
            self.walkimage = pygame.image.load(os.path.join("images\walking", direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()
              #Blit it here instead of the draw method for better clarity
            self.walkimage.set_colorkey(self.image.get_at((0,0)))
            if (time -self.starttime > 0.7):
               # Update time every 2.1 ish seconds
               
               self.changetime(time)
            
                       
               if self.cursor >7*frame:
                  # If the animation frame is greater than seven (only seven walking animation frames) then reset the cursor
                  self.cursor = 1
               # change animation frame as per the animation cursor
              
                 
                  

               if self.cursor <=7*frame:
                  #Move the Animatioon framecursor as long as it is below the frame amount
                  self.cursor +=1
               if self.cursor >7*frame:
                  self.cursor = 1
               if self.cursor in(5*frame,frame):
                  
                  self.cursor += (round(frame/1.5))
              
                  
          
      else:
         #If its not in a going state change the image to the defualt reserve image
         
         self.image = self.imageres
         self.mining ==False

      
   def unmine(self):
      self.mining = False
      if self.minepos is not None and self.targetmine != None:
         #print(" I am unmining ")
         self.targetmine.unmark(self.minepos)
   def unchop(self):
      self.chopping = False
      if self.choppos is not None and self.targettree is None:
         #print(" I am unmining ")
         self.targettree.unmark(self.choppos)
  
   def update(self,citizenlst):
      '''
      ENsures the citizen does not ram into another instance of itself or leave the screen      
      '''
      ls = []
      
      self.citizenlst = citizenlst.copy()
      for citizen in self.citizenlst:
         if citizen is not self:
            if citizen.getCollisionRect().colliderect(self.getCollisionRect()):
               
               
               if self.mining == False and citizen.going==False and citizen.going ==True:
                  self.position.x +=8
                  self.position.y+=3
                  # self.end[0]+=10
                  # self.end[1] +=5
                  
               if citizen.mining == False and self.going ==False and self.going == True:
                  citizen.position.x -= 8
                  citizen.position.y -=3
                  
                  # citizen.end[0]-=8
                  # citizen.end[1] -=3

               self.citizenlst.remove(citizen)
   def build(self,clock):
      if self.building == True and self.arrived ==True:
               
         frame = 12
         time = clock.get_ticks()/100
         if self.building == True and self.arrived ==True:
            
         
               if (abs(self.starttime-time)> 2):
                  self.changeminetime(time) 
               
         
                        
                  
                  # Draw the mining citizen ( Drawing it here instead of Draw method because of increased clarity)
                  self.buildimage = pygame.image.load(os.path.join("images\Construction","building" +str(max(1,round(self.buildcursor/frame)))+".png")).convert()
                  self.buildimage.set_colorkey(self.image.get_at((0,0)))
                  #surface.blit(self.image, list(self.position))
                  #self.image.set_colorkey(self.image.get_at((0,0)))
                  
                  # There are 9 animation frames with a wait time of 6 frames, so whenever the frame cursor is above 54, it recurses back to one
                  if self.buildcursor <=5*frame:
                     self.buildcursor +=1
                  
                  
                  if self.buildcursor >3*frame:
                     self.struct.advance(self.buildrate,self)
                     self.buildcursor = 1
                  if self.buildcursor ==3*frame:
                     
                     self.chopsound.play()
            
         else:
            
            # Set it to the reserve image
            self.image = self.imageres
            self.mining ==False

            
   def stopbuilding(self):
      self.building = False 

     
               
         
         


        
