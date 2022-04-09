from vector2D import Vector2
from physics import Distance,rad
from drawable import drawable
from Panel import panel
from character import Character
import os
import pygame
from projectile import Projectile
import math


Bonus = {"Pikeman":-10, "Rifleman":-10,"Building":-30,"Cavalry":-190,"Cannon":0}
class cannon(Character):
    def __init__(self,color,xposition,yposition):
        if color =="Green":
            self.color = "green"
            path = os.path.join("images\Cannon" +"\Green", "90walking1.png")
        
        else:
           self.color = "Red"
           path = path = os.path.join("images\Cannon\Red", "90walking1.png")

        super().__init__(path,xposition,yposition)
        self.shootcursor =1
        self.walkcursor =1
        self.shooting = False
        self.going = False
        self.imageres = self.image
        self.walkimage = self.image
        self.shootimage = self.image
        self.attack = 80
        self.HP = 130
        self.type = "Cannon"
        self.frame = 2

        self.veradjust = 30

        self.shootsound = pygame.mixer.Sound(os.path.join("sound","cannonshooting.wav"))

        self.direction = "0"
        self.moving = True


        self.rangeimage = os.path.join("images\Cannon","riflerangerect.png")
        self.verimage= os.path.join("images\Cannon","uprange.png")
        self.radarimage = os.path.join("images","radar.png")


       ####Sensing the direction
      

        self.rangeup = panel(self.verimage,self.verimage,0,0)
        self.rangedown = panel(self.verimage,self.verimage,0,0)
        self.rangeright = panel(self.rangeimage,self.rangeimage,0,0)
        self.rangeleft = panel(self.rangeimage,self.rangeimage,0,0)
        self.collisionim =os.path.join("images\Rifleman","cannoncollisionrect.png")
        self.collideim = panel(self.collisionim,self.collisionim,0,0)
        self.radar= drawable(self.radarimage,0,0)

        self.rangelst = [self.rangeup,self.rangedown,self.rangeright,self.rangeleft]


               
    def goshoot(self,target =None):
       self.target = target
       self.shooting = True
    def shoot(self,clock,projectilelst,enemylst,framerate = 2):
      ''''
      Walks the citizen as per the requested frame rate      
      '''
      
      time = clock.get_ticks()/1000

      

      frame =9

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
      
      
 

      spotted= False
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
               self.end[0]= target.getPosition().x

            else:
               self.end[1]= target.getPosition().y



            

         

         







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
            if self.color == "Red":
               self.shootimage = pygame.image.load(os.path.join("images\Cannon\Red", direction+"shooting"+str(max(1,round(self.shootcursor/frame)))+".png")).convert()
              #Blit it here instead of the draw method for better clarity
            else:
               self.shootimage = pygame.image.load(os.path.join("images\Cannon\Green", direction+"shooting"+str(max(1,round(self.shootcursor/frame)))+".png")).convert()
            
              #Blit it here instead of the draw method for better clarity
            self.shootimage.set_colorkey(self.image.get_at((0,0)))
            #rint("difference " + str(abs(time -self.starttime )))
            if abs(time -self.starttime) >0.01:
            #    # Update time every 2.1 ish seconds
               
               self.changetime(time)

               #rint("updating " + str(self.shootcursor) + "print this is max " + str(frame*16))
            
                       
               if self.shootcursor >16*frame:
                     # If the animation frame is greater than seven (only seven walking animation frames) then reset the cursor
                     self.shootcursor = 1
                  # change animation frame as per the animation cursor
               
                  
                     

               elif self.shootcursor <=16*frame:
                     #Move the Animatioon framecursor as long as it is below the frame amount
                     self.shootcursor +=1
            
                     
               if self.shootcursor == 14*frame:
                  pygame.mixer.set_num_channels(100)
                  if direction =="90":
                     bullet = Projectile(self.position.x+135,self.position.y+31,400,int(direction),enemylst)

                  if direction =="180":
                     bullet = Projectile(self.position.x+86,self.position.y+89,400,int(direction),enemylst)

                  if direction =="0":
                     bullet = Projectile(self.position.x-10+0.33*self.getWidth(),self.position.y-self.getHeight(),400,int(direction),enemylst)
                  if direction == "270":
                  
                     bullet = Projectile(self.position.x-10,self.position.y+10,400,int(direction),enemylst)
                  bullet.changetocannon()
                  bullet.attack = self.attack
                  bullet.attack += Bonus[target.type]
                  if target.type =="Building":
                     bullet.attack = 30
                  projectilelst.append(bullet)
                  channel = pygame.mixer.find_channel()
                  #rint("AM I empty"  + str(channel ==None))

                  
                  
                  if channel is not None:
                        #rint(" THis is busy " + str(channel.get_busy()))
                        channel.set_volume(0.8)
                        channel.play(self.shootsound)
                  
                     


    def beginmoving(self,end):
      '''
      Initializes the go method with the appropriate end variable
      '''
    
      self.going = True
      #self.selected = False
      self.shooting = False
      self.start = list(self.position)
      start = self.start
      self.end = end
   


    def getCollisionRect(self):
      # oldrect = self.image.get_rect()
      # modified = oldrect.inflate(-2,-2)
      # newRect =  self.position + modified 
      return self.collideim.getCollisionRect()
    def updaterange(self):
      cpointy = self.position.y +self.centery*self.getHeight()  
      cpointx = self.position.x +self.centerx*self.getWidth() 

      

      self.rangeup.position.x = cpointx-11
      self.rangeup.position.y = cpointy-300

      self.rangedown.position.x = cpointx-6
      self.rangedown.position.y = cpointy+60

      self.rangeleft.position.x = cpointx-330
      self.rangeleft.position.y = cpointy-8


      self.rangeright.position.x = cpointx+20
      self.rangeright.position.y = cpointy-12
    def draw(self,surface):

       

        self.updatecollide()
        self.updaterange()
        #self.radar.draw(surface)
        #self.rangeup.draw(surface)
        #pygame.draw.rect(surface,(0,0,255),self.getCollisionRect())

          

        #for item in self.rangelst:
              #item.draw(surface)
           #print("this is x, " , str(item.position.x))
        #"Length of range " + str(len(self.rangelst)))

        #for item in self.sensorls:
           #item.draw(surface)
        if [self.dead,self.shooting,self.going] == [False,False,False]:
      #its in a nothing state here, doing nothing
         
         surface.blit(self.image, list(self.position))
         self.image.set_colorkey(self.image.get_at((0,0)))
         
        if self.selected == True:

           surface.blit(self.selectedim,[self.getPosition().x+34,self.getPosition().y-7])
         
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



    def walk(self,clock,framerate = 5):
      ''''
      Walks the citizen as per the requested frame rate      
      '''
      
      frame =framerate

      maxframe = 4
      #Weird time, but trial and error shows 28 is best for walking
      time = clock.get_ticks()/28

      #print("this is time: " + str(time) + " starttime : " + str(self.starttime)) 
      if self.going ==True: 

                  
            direction = self.getAnglestate()
            self.direction = direction

            
            if self.getAnglestate() not in ("270","180","90","0"):
               direction = "0"
               self.direction = direction
            if self.color == "Red":
               self.walkimage = pygame.image.load(os.path.join("images\Cannon\Red", direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()
              #Blit it here instead of the draw method for better clarity
            else:
               self.walkimage = pygame.image.load(os.path.join("images\Cannon\Green", direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()

            self.walkimage.set_colorkey(self.image.get_at((0,0)))
            if (time -self.starttime > 0.7):

               # Update time every 2.1 ish seconds
               
               self.changetime(time)
            
                       
               if self.cursor >maxframe*frame:
                  # If the animation frame is greater than seven (only seven walking animation frames) then reset the cursor
                  self.cursor = 1
               # change animation frame as per the animation cursor
              
                 
                  

               if self.cursor <=maxframe*frame:
                  #Move the Animatioon framecursor as long as it is below the frame amount
                  self.cursor +=1
               if self.cursor >maxframe*frame:
                  self.cursor = 1
               
              
                  
          
      else:
         #If its not in a going state change the image to the defualt reserve image
         
         self.image = self.imageres

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
    def updatecollide(self):

   
      cpointy = self.position.y +self.centery*self.getHeight()+19
      cpointx = self.position.x +self.centerx*self.getWidth()-8

      self.collideim.position.x = cpointx -30
      self.collideim.position.y = cpointy - self.veradjust
       
      
         

        
    
