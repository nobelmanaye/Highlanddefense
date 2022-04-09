

from doctest import ELLIPSIS_MARKER
import pygame
import os
import math
import random

from vector2D import Vector2
from physics import Distance,rad
from drawable import drawable
from Panel import panel
SCREEN_SIZE = Vector2(1440, 900)
WORLD_SIZE = Vector2(1440, 900)

class Character(drawable):

    def __init__(self,path,xposition,yposition):

        super().__init__(path,xposition,yposition)
        self.cursor = 1
        self.start = [0,0]
        self.end = [0,0]
        self.maxspeed = 30
        self.fixspeed = 30
        self.tolerance = 2
        self.going = False
        self.selected = False
        self.arrived = False
        self.HP = 100
        self.dead = False
        self.starttime = 1
        self.selectedim = pygame.image.load(os.path.join("images","selectedpointer.png")).convert()
        self.adjustimage =  os.path.join("images","mouse.png")
        self.rangeimage = os.path.join("images\Rifleman","riflerangerect.png")
        self.verimage= os.path.join("images\Rifleman","uprange.png")
        
        self.rangedownim = self.rangeimage
        self.rangerightim = self.rangeimage
        self.rangeleftim = self.rangeimage
        self.centerpos = self.position
       
        self.centerx = 0.5
        self.centery = 0.3
        self.adjust = 20
        self.veradjust= 30
        self.lastspeed = "down"
        self.lastpos = ""


        ######## Setting the "sensor" rectangles for path finding ##########
        self.up = panel(self.adjustimage,self.adjustimage,0,0)
        self.down= panel(self.adjustimage,self.adjustimage,0,0)
        self.left= panel(self.adjustimage,self.adjustimage,0,0)
        self.right = panel(self.adjustimage,self.adjustimage,0,0)

        self.rangeup = panel(self.verimage,self.verimage,0,0)
        self.rangedown = panel(self.verimage,self.verimage,0,0)
        self.rangeright = panel(self.rangeimage,self.rangeimage,0,0)
        self.rangeleft = panel(self.rangeimage,self.rangeimage,0,0)


        
       

       

        self.sensorls = [self.up,self.down,self.left,self.right]
        self.rangelst = [self.rangeup,self.rangedown,self.rangeright,self.rangeleft]
        
        self.xsensormin = 15
        self.ysensormin = 15
        self.xsensormax = 155
        self.ysensormax =155
        ####################Weird pathing states to help with pathing#########
        self.pathstate = ""

    
    def changespeed(self,end):
      self.start = list(self.position)
      start = self.start
      self.end = list(end)

      
      # Calculate the angle. 
      angle = rad(list(start),list(end))

      #adjust speed according to destination
      if start[1] < end[1]:
         self.velocity.y = abs(math.sin(angle)*self.maxspeed)
      if start[0] < end[0]:
         self.velocity.x = abs(math.cos(angle)*self.maxspeed)
      if start[0] > end[0]:
         self.velocity.x = -abs(math.cos(angle)*self.maxspeed)
      if start[1] >end[1]:
         self.velocity.y = -abs(math.sin(angle)*self.maxspeed)
    def changetime(self,time):
      '''
      Resets the time cursor used for animation
      '''
      self.starttime = time
    
    def updateadjust(self):
      cpointy = self.position.y +self.centery*self.getHeight()+19
      cpointx = self.position.x +self.centerx*self.getWidth()-8

      


      self.up.position.x = cpointx 
      self.up.position.y = cpointy - self.veradjust

      self.down.position.x = cpointx 
      self.down.position.y = cpointy + self.veradjust

      self.left.position.x = cpointx -self.adjust
      self.left.position.y = cpointy 

      self.right.position.x = cpointx + self.adjust
      self.right.position.y = cpointy 

      self.old = self.position

      

      
     

    def go(self,time,buildinglst,build = False):
      '''

      Updates the position of the orb so that it does not fall of the edge
      '''
      self.updateadjust()
      

      
      #Go only if its going

      colliding =False
      start = list(self.position)
      end = self.end
      xdiff = start[0]-end[0]
      ydiff = start[1]-end[1]
      
      if self.going == True and self.dead == False:

         

         
         # Check for collision, if there is, save the colliding building in collingbuild
         if len(buildinglst) > 0:
            for building in buildinglst:
               for sensor in self.sensorls:
                  if sensor.getCollisionRect().colliderect(building.getCollisionRect()):

                     colliding = True
                     collingbuild = building.getCollisionRect()


         #if colliding is activated, then go
         if colliding == True:
            if build:
               collide=False

               self.manualgo(time)


               


               
            else:

                  possdirections = []

                  adjust = self.adjust


                  #print(" This is xdiff "+ str(xdiff) + " This is ydiff " + str(ydiff))

                  #self.changespeed(end)
                  
                  

                  if collingbuild.colliderect(self.right.getCollisionRect()) != True:
                     #self.velocity.x = -self.maxspeed


                     #print("right")
                     possdirections.append("right")
                     #self.velocity.y = 0
                     colliding ==False
                     


                  if collingbuild.colliderect(self.down.getCollisionRect()) != True:
                     #self.velocity.x = 0
                     #print("down")
                     if collingbuild.collidepoint(self.down.position.x,self.down.position.y+self.maxspeed) != True:

                        possdirections.append("down")
                        #self.velocity.y = self.maxspeed
                        colliding = False

                  if collingbuild.colliderect(self.left.getCollisionRect()) != True:
                     #self.velocity.x = +self.maxspeed
                     #print("left")

                     
                        possdirections.append("left")
                        #self.velocity.y = 0
                        colliding = False

                  if collingbuild.colliderect(self.up.getCollisionRect()) != True:
                     #self.velocity.x = 0
                     #print("up")
                     if collingbuild.collidepoint(self.up.position.x,self.up.position.y-self.maxspeed) != True:

                        possdirections.append("up")
                        #self.velocity.y = self.maxspeed
                        colliding = False
                  
                  #print("This is diff " + str((xdiff,ydiff)))
                  adjustedspeed = self.calculatepath(possdirections,xdiff,ydiff)
                  #rint("========DIST: "+ str(round(Distance(start,end)-self.tolerance)))
                  if Distance(start,end)-self.tolerance > 36:
                     

                     self.velocity.x = adjustedspeed[0]
                     self.velocity.y = adjustedspeed[1]
                     oldpos = self.position
                     
                     self.position.y = oldpos.y + ((self.velocity.y)*time.get_time()/1000)
                     self.position.x = oldpos.x + ((self.velocity.x)*time.get_time()/1000)

                     self.old = self.position
                     return
                  else:
                     
                     self.velocity.x = 0
                     self.velocity.y = 0
                     self.going = False
                     return 

                  #rint("1   X Velocity : "+ str(round(self.velocity.x)) + " Y  Velocity" + str(round(self.velocity.y)))
                  #rint("CHanged   x direction : "+ str(round(self.position.x)) + " Y direction" + str(round(self.position.y)))
      
                 


                     
                        
         else:  


            # Render the start(the current position) and the end
           
            
            self.manualgo(time)
            
               
                                       
      else:
            # Its not going, So stop         
            self.going = False
            self.velocity.x = 0
            self.velocity.y = 0
            #rint("2 X Velocity : "+ str(self.velocity.x) + " Y  Velocity" + str(self.velocity.y))
            return

    def beginmoving(self,end):
      '''
      Initializes the go method with the appropriate end variable
      '''
      self.going = True
      self.selected = False
      self.start = list(self.position)
      start = self.start
      self.end = list(end)

    def select(self):
        '''
        Selects the gamepiece 
        '''

        # select the fool, change the image to a selected image
        self.selected = True
        self.image = self.selimage

       #self.image = slightly beiged image
    def unselect(self):
        '''
        Unselects the game piece
        '''

        # Unselect it 
        self.selected = False
        self.image = self.imageres





    def getAngle(self):
       if self.velocity.x != 0 and self.velocity.y != 0:
         Angle = math.atan((self.velocity.y/self.velocity.x))*180/(math.pi)
         return Angle
       elif self.velocity.x ==0:
          if self.velocity.y <0:
             return 0
          if self.velocity.y > 0:
             return 180 
       else:
          return 0
    def getAnglestate(self):
       angle = self.getAngle()
       if angle is None:
          angle = 0
       
       newangle = abs(angle)
       #print("this is angle"+ str(newangle))

       if self.velocity.x == 0 and self.velocity.y>0:
          return "180"
       if self.velocity.x == 0 and self.velocity.y<0:
          return "0"
       if self.velocity.y == 0 and self.velocity.x>0:
          return "90"
       if self.velocity.y == 0 and self.velocity.x<0:
          return "270"
       

       if self.velocity.x >0 and self.velocity.y > 0:
          if newangle < 15:
             #print(" state : 90")
             return "90"
          elif newangle > 55:
             
             #print(" state : 180")
             return "180"
          else:
             #print("state 135")
             return "90"
       if self.velocity.x <0 and self.velocity.y > 0:
          
          if newangle < 15 or (newangle > 55 and newangle < 60):
             #print(" state : 270")
             return "270"
          elif newangle > 82:
             #print(" state : 225")
             return "180"
          else:
             return "270"
       if self.velocity.x <0 and self.velocity.y < 0:
         
          if newangle < 12 :
             #print(" state : 01")
             return "270"
          elif newangle < 50:
             #print(" state : 315")
             return "270"
          else: 
             return "0"
       if self.velocity.x >0 and self.velocity.y < 0:
          #print("should be here")
          if newangle >55: 
             #print(" state : 0")
             return "0"
          else:
             #print(" state : 45")
             return "90"
   
    def calculatepath(self,paths,xdiff,ydiff):

       pats =''
       max = self.maxspeed

       speeddict = {"right":[max,0],"up":[0,-max],"down":[0,max],"left":[-max,0]}

       if self.pathstate =="2":
          
                 
          if xdiff < 0 and "right" in paths:
             self.pathstate = ""
             #print("right1")
             self.lastspeed = "right"
             return speeddict["right"]
             
          if xdiff > 0 and "left" in paths:
             self.pathstate = ""
             #print("left1")
             self.lastspeed = "left"
             return speeddict["left"]
             
          if ydiff <self.ysensormin and "down" in paths:
             #print("down1")
             self.lastspeed = "down"
             return speeddict["down"]

         #  if ydiff >=self.ysensormin and "up" in paths:
         #     print("up")
         #     return speeddict["up"]
       
       if self.pathstate == "2":
          ##pri#nt(self.lastspeed + "2")
          return speeddict[self.lastspeed]
       elif self.pathstate =="1":
          if ydiff < 0 and "down" in paths:
             self.pathstate = ""
             self.lastspeed = "down"
             #print("down2")
             return speeddict["down"]
             
          if ydiff > 0 and "up" in paths:
             self.pathstate = ""
             self.lastspeed = "up"
             #print("up2")
             return speeddict["up"]
             
          if xdiff <=0 and "left" in paths:
             self.lastspeed = "left"
             #print("left2")
             return speeddict["left"]

          elif xdiff >=0 and "right" in paths:
             self.lastspeed = "right"
             
             #print("right2")
             return speeddict["right"]
      

     

      
       if abs(xdiff)< self.xsensormin and abs(ydiff) > self.ysensormax:
          self.pathstate = "1"
         
       if abs(xdiff)> self.xsensormax and abs(ydiff) < self.ysensormin:
          
          self.pathstate = "2"
      
          
       #p#rint("selfstate is " + self.pathstate)
       if self.pathstate != "":
          return speeddict[self.lastspeed]

       if xdiff >0 and ydiff >0 and self.pathstate =="":
          priority = ["up","left","down","right"]
          index = 0
          while True and index < len(priority):
             if priority[index] in paths:

                for string in paths:
                   pats += (" ,"+string)
                #print(" This is speed1 "  + priority[index] + " " + pats)
                
                if Character.isopposite(self.lastspeed,priority[index]):
                   return speeddict[self.lastspeed]
                else:
                  self.lastspeed = priority[index]
                  return speeddict[priority[index]]
                
             index += 1
      

             
         
       elif xdiff <0 and ydiff <0 and self.pathstate =="":
          priority = ["down","right","left","up"]
          index = 0
          while True and index < len(priority):
             if priority[index] in paths:
                for string in paths:
                   pats += (" ,"+string)
                #" This is speed2 "  + priority[index] + " " + pats)
                if Character.isopposite(self.lastspeed,priority[index]):
                   return speeddict[self.lastspeed]
                else:
                  self.lastspeed = priority[index]
                  return speeddict[priority[index]]
             index += 1
      
       elif xdiff <0 and ydiff >0 and self.pathstate =="":
          priority = ["up","right","down","left"]
          index = 0
          while True and index < len(priority):
             if priority[index] in paths:
                for string in paths:
                   pats += (" ,"+string)
                #print(" This is speed3 "  + priority[index] + " " + pats)
                if Character.isopposite(self.lastspeed,priority[index]):
                   return speeddict[self.lastspeed]
                else:
                  self.lastspeed = priority[index]
                  return speeddict[priority[index]]
             index += 1

       elif xdiff >0 and ydiff <0 and self.pathstate =="":
          
          priority = ["left","up","right"]
          if self.lastspeed == "up":
             priority = ["left", "down","left","up","right"]
          index = 0
          while True and index < len(priority):
             if priority[index] in paths:
                pats = ' '
                for string in paths:
                   pats += (" ,"+string)
                
                
                if Character.isopposite(self.lastspeed,priority[index]):
                   #print(" This is mod speed4 "  + self.lastpos + " " + pats)
                   return speeddict[self.lastspeed]
                else:
                  #print(" This is speed4 "  + priority[index] + " " + pats)
                  self.lastspeed = priority[index]
                  return speeddict[priority[index]]
             index += 1
       
         
       return speeddict[self.lastspeed]
      


    
       


            
       
       
       
       



    def isopposite(speed1,speed2):
      if speed1 in ["left","right"] and speed2 in ["left","right"]:
         return speed1 !=speed2
      if speed1 in ["up","down"] and speed2 in ["up","down"]:
         return speed1 != speed2
      else:
         return False
      

       

    def isselected(self):
        '''
        Returns the state of selection, or unselection
        '''
        return self.selected

   
    def recvDamage(self,damage):
        self.HP -= damage
        if self.HP <= 0:
           self.dead = True
      
    def kill(self):
        '''
        Self explanatory. Blood will be spilled
        '''
        self.dead  =True

    def isDead(self):

        '''
        Checks for deadness.
        '''
        return self.dead

    def manualgo(self,time):
            start = list(self.position)
            end = self.end
        
            self.changespeed(end)

            difference = Distance(list(start),list(end))

            angle = rad(list(start),list(end))

            # If the citizen hasn't reached distination yet
               
            
            if Distance(start,end)>self.tolerance and self.going == True:
            
               self.arrived = False
               angle = rad(start,end)
            
            
            
               oldpos = self.position

               #Update the position
               newposy = oldpos.y + self.velocity.y*time.get_time()/1000
               newposx = oldpos.x +self.velocity.x*time.get_time()/1000


               # if is about to cross the screen, reverse the velocity
               if newposy+self.getHeight() > WORLD_SIZE.y:

                  self.velocity.y *=-1

               elif newposy <0:

                  self.velocity.y *=-1

               if newposx +self.getWidth()> WORLD_SIZE.x:

                  self.velocity.x *=-1


               elif newposx <0:

                  self.velocity.x *=-1


               self.position.y = oldpos.y + ((self.velocity.y)*time.get_time()/1000)
               self.position.x = oldpos.x + ((self.velocity.x)*time.get_time()/1000)
                
               #rint("X Velocity 5: "+ str(round(self.velocity.x)) + " Y  Velocity" + str(round(self.velocity.y)))
               #rint(" AFTER  X : " + str(round(self.position.x)) + " Y : "+ str(round(self.position.y)) )
               return
              

               
            else:
               #reached desitation,stop going, and unselect, flag the arrived variable for event
               
               self.going =False
               self.updated = False
               self.unselect()
               #Stop
               self.velocity.x = 0
               self.velocity.y = 0
               
               self.arrived = True



ls = [("left","right")]
for item in ls: 
   print(Character.isopposite(item[0],item[1]))


               
                                       
           
          


              
