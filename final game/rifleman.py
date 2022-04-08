
from doctest import ELLIPSIS_MARKER
import pygame
import os
import math
import random
from vector2D import Vector2
from physics import Distance,rad
from projectile import Projectile
from Panel import panel


from character import Character

from drawable import drawable

Bonus = {"Cannon":10, "Pikeman":13,"Building":-8,"Cavalry":5,"Rifleman":10}
class Rifleman(Character):

    def __init__(self,path,xposition,yposition,color="Green"):
        self.color = color
        super().__init__(path,xposition,yposition)
        if self.color == "Green":
         path=  os.path.join("images\Rifleman\Green\Walking","180walking1.png")
        else:
         path = os.path.join("images\Rifleman\Red\Walking","180walking1.png")
        self.walking = False
        self.imageres = self.image
        self.shooting = False
        
        self.shootingimage = self.imageres
        self.starttime =1
        self.shootcursor = 1
        self.cocksound = pygame.mixer.Sound(os.path.join("sound","cocking.wav"))
        self.shootsound = pygame.mixer.Sound(os.path.join("sound","rifleshooting.wav"))
        self.type = "Rifleman"
        

    def quickshootfix(self,color):
       
       self.collisionim =os.path.join("images\Rifleman","riflecollisionrect.png")
       self.collideim = panel(self.collisionim,self.collisionim,0,0)
       self.walkimage = self.image
       self.shootimage = self.image
       self.shooting = False
       self.shootcursor = 1
       self.noshoottime = 0
       self.color = color

       self.moving = False

       self.cocksound = pygame.mixer.Sound(os.path.join("sound","cocking.wav"))
       self.shootsound = pygame.mixer.Sound(os.path.join("sound","rifleshooting.wav"))

       self.direction = "0"
       self.enemy = None
       self.range = 200
       self.cost= [0,25]

       self.veradjust= 30
       self.adjust= 20

       ###########Sesning the enemy
       self.rangeimage = os.path.join("images\Rifleman","riflerangerect.png")
       self.verimage= os.path.join("images\Rifleman","uprange.png")

       ####Sensing the direction
      

       self.rangeup = panel(self.verimage,self.verimage,0,0)
       self.rangedown = panel(self.verimage,self.verimage,0,0)
       self.rangeright = panel(self.rangeimage,self.rangeimage,0,0)
       self.rangeleft = panel(self.rangeimage,self.rangeimage,0,0)

       

       self.rangelst = [self.rangeup,self.rangedown,self.rangeright,self.rangeleft]
       self.radarimage = os.path.join("images","radar.png")
       self.radar= drawable(self.radarimage,0,0)





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
      
    def getCollisionRect(self):
       oldrect = self.collideim.getCollisionRect()
       
       return oldrect


    def updatecollide(self):
      cpointy = self.position.y +self.centery*self.getHeight()+19
      cpointx = self.position.x +self.centerx*self.getWidth()-8

      self.collideim.position.x = cpointx 
      self.collideim.position.y = cpointy - self.veradjust
       



    def draw(self,surface):
        
        self.updatecollide()
        self.updaterange()
        #self.rangeup.draw(surface)
        #pygame.draw.rect(surface,(0,0,255),self.getCollisionRect())

          

      #   for item in self.rangelst:
      #        item.draw(surface)
           #print("this is x, " , str(item.position.x))
        #"Length of range " + str(len(self.rangelst)))

        #for item in self.sensorls:
           #item.draw(surface)
        if [self.dead,self.shooting,self.going] == [False,False,False]:
      #its in a nothing state here, doing nothing
         
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))
         
        if self.selected == True:

           surface.blit(self.selectedim,[self.getPosition().x+16,self.getPosition().y-7])
         
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


         

    def updaterange(self):
      cpointy = self.position.y +self.centery*self.getHeight()  
      cpointx = self.position.x +self.centerx*self.getWidth() 

      self.radar.position.x = cpointx -self.radar.getWidth()*0.5
      self.radar.position.y = cpointy - self.radar.getHeight()*0.5

      self.rangeup.position.x = cpointx-6
      self.rangeup.position.y = cpointy-300

      self.rangedown.position.x = cpointx-6
      self.rangedown.position.y = cpointy+60

      self.rangeleft.position.x = cpointx-330
      self.rangeleft.position.y = cpointy-8


      self.rangeright.position.x = cpointx+20
      self.rangeright.position.y = cpointy-12

    def goshoot(self,target =None):
       self.target = target
       self.shooting = True

    def shoot(self,clock,projectilelst,enemylst,framerate = 5):
      ''''
      Walks the citizen as per the requested frame rate      
      '''
     
      time = clock.get_ticks()/28

      
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

            if xdiff < ydiff:
               old = list(self.end)
               old[0]= target.getPosition().x
               self.end = old

            else:
               old = list(self.end)
               old[1]= target.getPosition().y
               self.end = old


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

            if self.color== "Green":
                  self.shootimage = pygame.image.load(os.path.join("images\Rifleman\Green\Shooting", direction+"shooting"+str(max(1,round(self.shootcursor/frame)))+".png")).convert()
            else:
                  self.shootimage = pygame.image.load(os.path.join("images\Rifleman\Red\Shooting", direction+"shooting"+str(max(1,round(self.shootcursor/frame)))+".png")).convert()
            self.shootimage.set_colorkey(self.image.get_at((0,0)))
            #print("difference " + str(abs(time -self.starttime )))
            # if abs(time -self.starttime) > 0.7:
            #    # Update time every 2.1 ish seconds
               
            #    self.changetime(time)
            
                       
                    

            if self.shootcursor <=14*frame:
                     #Move the Animatioon framecursor as long as it is below the frame amount
                     self.shootcursor +=1
            if self.shootcursor >14*frame:
                     self.shootcursor = 1

            if self.shootcursor == 10*frame:
                     bullet = Projectile(self.position.x-10,self.position.y+10,400,int(direction),enemylst)

                     bullet.attack += Bonus[target.type]
                     projectilelst.append(bullet)
                     channel = pygame.mixer.find_channel()
                     if channel is not None and channel.get_busy() != True:
                        channel.set_volume(0.4)
                        channel.play(self.shootsound)

            if self.shootcursor == 2*frame:
                     
                     channel = pygame.mixer.find_channel()
                     
                     
                     delay = random.randint(1,3)
                     if channel is not None and channel.get_busy() != True and delay ==2:
                        channel.set_volume(0.2)
                        channel.play(self.cocksound)

                  
            if self.cursor in(5*frame,6*frame,7*frame):
                     
                      delay = random.randint(1,5)
                      if delay == 4:

                        self.cursor -= round(0.75*frame)
               
                     

                   
    def updateadjust(self):
      cpointy = self.position.y +self.centery*self.getHeight()+19
      cpointx = self.position.x +self.centerx*self.getWidth()-2

      


      self.up.position.x = cpointx 
      self.up.position.y = cpointy - self.veradjust

      self.down.position.x = cpointx 
      self.down.position.y = cpointy + self.veradjust

      self.left.position.x = cpointx -self.adjust
      self.left.position.y = cpointy 

      self.right.position.x = cpointx + self.adjust
      self.right.position.y = cpointy 

      self.old = self.position

       

    def walk(self,clock,framerate = 7):
      ''''
      Walks the citizen as per the requested frame rate      
      '''
      
     
      frame =8

      #Weird time, but trial and error shows 28 is best for walking
      time = clock.get_ticks()/28

      #print("this is time: " + str(time) + " starttime : " + str(self.starttime)) 
      if self.going ==True: 

                  
            direction = self.getAnglestate()
            self.direction = direction

            
            if self.getAnglestate() not in ("270","180","90","0"):
               direction = "0"
               self.direction = direction
               
            if self.color== "Green":
                  
                  self.walkimage = pygame.image.load(os.path.join("images\Rifleman\Green\Walking", direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()
            else:
                 
                  self.walkimage = pygame.image.load(os.path.join("images\Rifleman\Red\Walking", direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()

                #Blit it here instead of the draw method for better clarity
            self.walkimage.set_colorkey(self.image.get_at((0,0)))

           
            if (time -self.starttime >0.3):
               
               
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
         
