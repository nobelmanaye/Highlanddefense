from email.mime import image

from doctest import ELLIPSIS_MARKER
import pygame
import os
import math
import random

from Physics.physics import Distance,rad
from Physics.drawable import drawable

class Projectile(drawable):

    def __init__(self,xposition,yposition,velocity = 300,angle = 90,enemies=None,damage=10):
        path = os.path.join("images\Projectiles","riflebullet.png")
        collidepath = os.path.join("images\Projectiles","bullet_collideim.jpg")
        self.dead = False 
        self.angle = angle
        self.enemies = enemies
        self.attack = damage
      
        self.shell = False
        self.start = [xposition,yposition]
        self.range =240
        self.velocity = 0
        self.angle = angle
    
        self.collideim =drawable(collidepath,xposition,yposition,)
        super().__init__(path,xposition,yposition)
        if not self.shell:
            rad = angle*math.pi/180
            res = pygame.transform.rotate(self.image,270)
            self.image =res

            res = pygame.transform.rotate(self.image,int(angle))
            self.image = res

        if angle ==0:
            self.velocity.y = -velocity
            self.velocity.x = 0
            
            self.position.x += 27
            self.position.y += 10
        if angle == 180:
            self.velocity.y = velocity
            self.position.x += 32
            self.position.y += 10
        

        if rad !=0:
            self.velocity.x = math.cos(rad)*velocity
            self.velocity.x = math.sin(rad)*velocity
        
        
    
    def changetocannon(self):
        self.image = pygame.image.load(os.path.join("images\Projectiles","cannonball.png"))
        
        self.shell = True
        self.range = 360
    def multiply_speed(self, factor):
         angle = self.angle
         if angle in (0,180):
            self.velocity.y *= factor
         else:
            self.velocity.x *= factor
            


        
           
    def draw_collide_im(self,surface):
        self.collideim.draw(surface)
        
        self.collideim.image.set_colorkey(self.collideim.image.get_at((0,0)))
        
    def travel(self,time):
        oldpos = self.position
        newposy = oldpos.y + self.velocity.y*time.get_time()/1000
        newposx = oldpos.x +self.velocity.x*time.get_time()/1000
        self.position.x = newposx
        self.position.y = newposy

        
        self.collideim.position.x = self.position.x
        self.collideim.position.y= self.position.y
        if Distance(self.start,list(self.position)) > self.range:
                self.dead = True

        for enemy in self.enemies:

            if self.collideim.getCollisionRect().colliderect(enemy.getCollisionRect()):
                if enemy.type=="Building":
                 #  print("Recieving damage " + enemy.type  + " "+ str(self.attack))
                    enemy.recvDamage(self.attack)
            
                    self.dead = True

                else:
                     enemy.recvDamage(self.attack)
                     projectile_nm = "rifleman" if not self.shell else "cannon"
                     print( "Recieving damage from " + projectile_nm + " to "+enemy.type  + " "+ str(self.attack) )
                     self.dead = True

    def die(self):
        self.dead = True

        
    