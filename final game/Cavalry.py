
from doctest import ELLIPSIS_MARKER
import pygame
import os
import math
import random

from Cannon import cannon
from pikeman import Pikeman
from rifleman import Rifleman
from vector2D import Vector2
from physics import Distance,rad
from projectile import Projectile
from Panel import panel
from drawable import drawable
from character import Character

Bonus = {"Cannon":-10, "Rifleman":-8,"Building":-38,"Pikeman":-20,"Cavalry":0}

class cavalry(Character):
    def __init__(self,color,xposition,yposition):




        path = os.path.join('Images\Cavalry'+"\C"+color,"180walking1.png")
        self.collisionim =os.path.join("images\Cavalry","cavcollisionrect.png")
        self.collideim = panel(self.collisionim,self.collisionim,0,0)
        super().__init__(path,xposition,yposition)
        self.range= 30
        self.maxspeed = 60
        self.direction = "270"
        self.color= color
        self.shooting = False
        self.shootingcursor = 1
        self.imageres = self.image
        self.starttime =1
        self.shootingimage = self.image
        self.shootcursor = 1
        self.attack = 40
        self.HP = 150
        self.type = "Cavalry"

        self.rangeimage = os.path.join("images\Cavalry","up.png")
        self.verimage= os.path.join("images\Cavalry","side.png")
        self.walkimage = self.image

       ####Sensing the direction

        self.sword1 = pygame.mixer.Sound(os.path.join("sound","Sword1.wav"))
        self.sword2 = pygame.mixer.Sound(os.path.join("sound","Sword2.wav"))
      

        self.rangeup = panel(self.verimage,self.verimage,0,0)
        self.rangedown = panel(self.verimage,self.verimage,0,0)
        self.rangeright = panel(self.rangeimage,self.rangeimage,0,0)
        self.rangeleft = panel(self.rangeimage,self.rangeimage,0,0)

        self.rangelst = [self.rangeup,self.rangedown,self.rangeright,self.rangeleft]

        self.radarimage = os.path.join("images","radar.png")
        self.radar= drawable(self.radarimage,0,0)

    def goshoot(self,target =None):
       self.target = target
       self.shooting = True

    def shoot(self,clock,projectilelst,enemylst,framerate = 2):
      ''''
      Walks the citizen as per the requested frame rate      
      '''
      
      time = clock.get_ticks()/1000

      

      frame =7

      distancedict = {}

      sortedenemy = []
      
      self.shootimage = self.image

      self.shooting = False
      for enemy in enemylst:
         xdiff = self.getPosition().x -enemy.getPosition().x
         ydiff = self.getPosition().y -enemy.getPosition().y
         xdiff= min(xdiff, 0.0001)
         angle = (abs(math.atan(ydiff/xdiff)))*180/(math.pi)
         
      
         for rect in self.rangelst:
            if enemy.getCollisionRect().colliderect(rect.getCollisionRect()):
               distance = Distance(list(enemy.getPosition()),list(self.getPosition()))
               self.shooting = True
               self.going = False
               self.starttime = 0
               

               distancedict[distance]=enemy
               sortedenemy.append(distance)
        
      start = list(self.position)
      if Distance(start,self.end)-self.tolerance > 36 and self.shooting != True:
         self.going = True  

      spotted = False

      if self.shooting!= True and self.going !=True:
         distancedict = {}

         sortedenemy = []
         for enemy in enemylst:
            if enemy.getCollisionRect().colliderect(self.radar.getCollisionRect()):
               distance = Distance(list(enemy.getPosition()),list(self.getPosition()))
               spotted = True
               distancedict[distance]=enemy
               sortedenemy.append(distance)

         if spotted:
            sortedenemy.sort()
            


            target = distancedict[sortedenemy[0]]

            xdiff = self.getPosition().x -target.getPosition().x
            ydiff = self.getPosition().y -target.getPosition().y

            
            self.end[0]= target.getPosition().x

            
            self.end[1]= target.getPosition().y
            self.end[0] = target.getPosition().x

      if self.shooting:
            sortedenemy.sort()
            


            target = distancedict[sortedenemy[0]]

            if target.getCollisionRect().colliderect(self.rangeup.getCollisionRect()):
               direction = "0"

            elif target.getCollisionRect().colliderect(self.rangedown.getCollisionRect()):

               direction = "180"

            elif target.getCollisionRect().colliderect(self.rangeleft.getCollisionRect()):
               direction = "270"

            elif target.getCollisionRect().colliderect(self.rangeright.getCollisionRect()):
               direction = "90"
            else:
               direction = "0"
     
            #rint("This is self direction ", self.direction, "this is angle " + str(angle))
            self.shootimage = pygame.image.load(os.path.join("images\Cavalry" + "\C"+self.color ,str(direction) + "shooting" + str(max(1,round(self.shootcursor/frame)))+".png")).convert()
              #Blit it here instead of the draw method for better clarity
            self.shootimage.set_colorkey(self.image.get_at((0,0)))
            #rint("difference " + str(abs(time -self.starttime )))
            if abs(time -self.starttime) >0.3:
            #    # Update time every 2.1 ish seconds
               
               self.changetime(time)

               #rint("updating " + str(self.shootcursor) + "print this is max " + str(frame*16))
            
                       
               if self.shootcursor >4*frame:
                     # If the animation frame is greater than seven (only seven walking animation frames) then reset the cursor
                     self.shootcursor = 1
                  # change animation frame as per the animation cursor
               
                  
                     

               elif self.shootcursor <=4*frame:
                     #Move the Animatioon framecursor as long as it is below the frame amount
                     self.shootcursor +=1
            
                     
               if self.shootcursor == 3*frame:
                  channel = pygame.mixer.find_channel()
                  

                  
                  
                  if channel is not None:
                        
                        channel.set_volume(0.5)
                        choice = random.randint(0,1)
                        if choice:
                            channel.play(self.sword1)
                        else:
                            channel.play(self.sword2)

                  attack = Bonus[target.type]+self.attack
                  target.recvDamage(attack)





 

    def updatecollide(self):
      cpointy = self.position.y +self.centery*self.getHeight()+19
      cpointx = self.position.x +self.centerx*self.getWidth()-8

      self.collideim.position.x = cpointx-44
      self.collideim.position.y = cpointy - self.veradjust

    def beginmoving(self,end):
      '''
      Initializes the go method with the appropriate end variable
      '''
      
      self.going = True
      self.selected = False
      self.shooting = False
      self.start = list(self.position)
      start = self.start
      self.end = end

    def draw(self,surface):

        # #self.updatecollide()
        #pygame.draw.rect(surface,(0,0,255),self.getCollisionRect())  
        # for item in self.sensorls:
        #   item.draw(surface)


        
        self.updatecollide()
        self.updaterange()
        #for item in self.rangelst:
             #item.draw(surface)
        if [self.dead,self.shooting,self.going] == [False,False,False]:
      #its in a nothing state here, doing nothing
         
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))

         
        if self.selected == True:

           surface.blit(self.selectedim,[self.getPosition().x+40,self.getPosition().y-12])
         
           self.selectedim.set_colorkey(self.selectedim.get_at((0,0)))

         
        
        if self.shooting == True and self.going == True:
           self.shooting=False
           self.image = self.walkimage
           surface.blit(self.image, list(self.position))
           self.image.set_colorkey(self.image.get_at((0,0)))
         
        elif self.shooting ==True:
           self.image = self.shootimage
           surface.blit(self.image, list(self.position))
           self.image.set_colorkey(self.image.get_at((0,0)))



        if self.going == True and self.shooting == False:
         
         self.image = self.walkimage
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))


    def walk(self,clock,framerate = 4):
      ''''
      Walks the citizen as per the requested frame rate      
      '''
      


      frame =framerate

      #Weird time, but trial and error shows 28 is best for walking
      time = clock.get_ticks()/28



      #print("this is time: " + str(time) + " starttime : " + str(self.starttime)) 
      if self.going ==True: 

                  
            direction = self.getAnglestate()
            self.direction = direction

            
            if self.getAnglestate() not in ("270","180","90","0"):
               direction = "0"
               self.direction = direction
            self.walkimage = pygame.image.load(os.path.join("images\Cavalry" + "\C"+self.color, direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()
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
         
    
    





#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    def goshoot(self,target =None):
       self.target = target
       self.shooting = True


    def updaterange(self):
      cpointy = self.position.y +self.centery*self.getHeight()  
      cpointx = self.position.x +self.centerx*self.getWidth()

      self.radar.position.x = cpointx -self.radar.getWidth()*0.5
      self.radar.position.y = cpointy - self.radar.getHeight()*0.5 

      self.rangeup.position.x = cpointx-30

      self.rangeup.position.y = cpointy-39

      self.rangedown.position.x = cpointx-30
      self.rangedown.position.y = cpointy+50


      self.rangeleft.position.x = cpointx-46
      

      self.rangeleft.position.y = cpointy


      self.rangeright.position.x = cpointx+20
      self.rangeright.position.y = cpointy
   
    def getCollisionRect(self):
      # oldrect = self.image.get_rect()
      # modified = oldrect.inflate(-2,-2)
      # newRect =  self.position + modified 
      return self.collideim.getCollisionRect()



