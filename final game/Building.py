import pygame
from Cannon import cannon
from vector2D import Vector2
from physics import Distance,rad
from citizen import Citizen
from drawable import drawable
from rifleman import Rifleman
from pikeman import Pikeman
from Cavalry import cavalry
import os 
from Panel import panel

costregister = {"rifleman":[0,30], "citizen":[0,5],"pikeman":[10,5],"cavalry":[0,80],"cannon":[100,300]}

class building(object):
   '''
   Implements the Orb object
   '''

   def __init__(self,selected,selecteddir,path,pathdir,xposition,yposition,progress= ''):
      '''
      initializes the Orb oject
      '''


      
      #initialize variables
      self.type = "Building"
      self.inflate = None
      
      
      self.velocity = Vector2(0,0)
      self.position = Vector2(0,0)
      self.position.x = xposition
      self.position.y = yposition
      self.blueprintx  = xposition
      self.blueprinty = yposition

      self.progress = progress
      self.maxprogress = 5
      
      
      self.buildcount = 1
      self.pathdir = pathdir
      self.pathname=path
      self.path = os.path.join(pathdir,path + str(self.progress) +".png")
     
      #print("this is selected  :" + selected)
      self.selectedpath = os.path.join(selecteddir,selected+ ".png")
      
      
      self.reserveimage = pygame.image.load(self.path).convert()
      self.selectedimage = pygame.image.load(self.selectedpath).convert()
      self.image = self.reserveimage
      self.collideimage = self.reserveimage
      self.blueprint = self.reserveimage
      self.dead = False
      self.buildlevel = 0
      self.unitdict = {"citizen":Citizen, "rifleman":Rifleman,"pikeman":Pikeman,"cavalry":cavalry,"cannon":cannon}
      self.homecollidepath = os.path.join("images/Buildings","homecollide.png")
      self.selected = False
      #generate starting conditions for the orb(including random desired speeds, velocity & position vecs)
      
      self.flagx = self.position.x-200
      self.flagy = self.position.y-200      
      
      self.spot = [-28 + self.position.x,-18+self.position.y]

      self.spots = [[self.position.x,self.position.y+self.image.get_height()]]
      
     
      self.gathererlst = [0 for x in range(len(self.spots))]

      self.HP = 300
      
      
      
      self.homecollide = panel(self.homecollidepath,self.homecollidepath,0,0)

   def setflagpos(self,flagx,flagy):
       self.flagx = flagx
       self.flagy = flagy

   def spawn(self,spawnunit,register):
       riflepath = os.path.join("images\Rifleman\Green\Walking","180walking1.png")
       if spawnunit == "rifleman":
          if register.existsenough(costregister["rifleman"][0],costregister["rifleman"][1]):
          
            return self.unitdict[spawnunit](riflepath,self.position.x-40, self.position.y-40)
          else:
             return False
       if spawnunit == "pikeman":
          if register.existsenough(costregister["pikeman"][0],costregister["pikeman"][1]):
            return self.unitdict[spawnunit]("Green",self.position.x-40, self.position.y-40)
          else:
             return False
       if spawnunit == "cavalry":
          if register.existsenough(costregister["cavalry"][0],costregister["cavalry"][1]):
            return self.unitdict[spawnunit]("Green",self.position.x-40, self.position.y-40)
          else:
             return False
       if spawnunit == "cannon":
          if register.existsenough(costregister["cannon"][0],costregister["cannon"][1]):
            return self.unitdict[spawnunit]("Green",self.position.x-40, self.position.y-40)
          else:
             return False
       
          
       if register.existsenough(costregister["citizen"][0],costregister["citizen"][1]):
         return self.unitdict[spawnunit](self.position.x+10, self.position.y+10)
       else:
          return False
       

   def recvDamage(self,damage):
        self.HP -= damage
        if self.HP <= 0:
           self.dead = True
   def update(self):
       self.path = os.path.join(self.pathdir,self.pathname +str(self.progress)+ ".png")
       self.image = pygame.image.load(self.path)
       self.image.set_colorkey(self.image.get_at((0,0)))
       

   def draw(self,surface):


      #pygame.draw.rect(surface,(0,0,255),self.getCollisionRect())

      if self.dead == False and self.selected ==False:
   
         #self.actualimage = pygame.image.load(self.pathlst[self.progress]).convert()
         surface.blit(self.image, list(self.position))
        
         self.image.set_colorkey(self.image.get_at((0,0)))
         
      elif self.selected == True and ((self.maxprogress == self.progress) or (self.progress == '')):
         
         surface.blit(self.selectedimage,list(self.position))
         self.selectedimage.set_colorkey(self.selectedimage.get_at((0,0)))
      else:
          surface.blit(self.image, list(self.position))
        
          self.image.set_colorkey(self.image.get_at((0,0)))
      


   def select(self):
       self.selected = True
       self.image = self.selectedimage
   def unselect(self):
       self.selected = False
       self.image = self.reserveimage

   def advance(self,buildrate,citizen):
       if self.progress ==self.maxprogress:
           citizen.building =False
       else:
           self.buildcount += buildrate
           self.progress = round(self.buildcount/10)


   def isselected(self):
       return self.selected
   def getgatherspot(self):
       return self.spot
    
   def markandgobuild(self,builder):

       
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
             builder.beginmoving(self.spots[copygatherer.index(item)])
             return 
   def getbuildspot(self):
       return self.position + self.getHeight()
   def kill(self):
      self.dead  =True
   def isDead(self):
      return self.dead
    
   
    





#======================drawable methods ===================


   def getX(self):

      return self.position.x


   def drawblueprint(self,surface,suitable,buildtype):
      
      if suitable:

         self.blueprint = pygame.image.load(os.path.join("images\Buildings", buildtype + "green.png")).convert()
         
      else:
          self.blueprint = pygame.image.load(os.path.join("images\Buildings", buildtype + "red.png")).convert()
      

      self.blueprintx = pygame.mouse.get_pos()[0]
      self.blueprinty = pygame.mouse.get_pos()[1]-self.image.get_height()
      self.image.set_colorkey(self.image.get_at((0,0)))
      surface.blit(self.blueprint,(self.blueprintx,self.blueprinty))
      
      

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

   def getPosition(self):
      '''
      Returns the positional vector of the orb
      '''
      return self.position
   
   def changecolliderect(self,imagepath):
      #rint("This is collide image" + str(self.collideimage))
      self.collideimage = imagepath
      
    
   
   def getCollisionRect(self,blueprint=False):
      #rint("this is slef.inflate" + str(self.inflate))
      home = False
      
      if type(self.progress) == int:
         self.collisionim = self.image

      else:
         #rint(" HHHHHEEEEEEEEEEEEEEERERERE")
         home = True
         self.collisionim = self.homecollide.image
      if not blueprint:
         oldrect = self.collisionim.get_rect()
      
      
         copy = Vector2(self.position.x,self.position.y+80)
         # copy.x += 10
         # copy.y += 10

         
         modified = oldrect
         if home:
               newRect =  copy + modified 
         else:
               newRect = self.position +modified

         return newRect
      else:
         copy = Vector2(self.blueprintx,self.blueprinty)
         oldrect = self.blueprint.get_rect()
         modified = oldrect
         newRect =  copy + modified


         return newRect 

         

         
         
   
      


   def drawcollide(self,screen):
      oldrect = self.image.get_rect()
      modified = oldrect

      newRect =  self.position + modified
      newRect.inflate(-0.5,1)
     
      pygame.draw.rect(screen,(255,255,255),newRect)
   
         
       
 



         
