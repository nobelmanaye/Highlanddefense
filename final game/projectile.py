from email.mime import image

from doctest import ELLIPSIS_MARKER
import pygame
import os
import math
import random
from vector2D import Vector2
from physics import Distance,rad
from drawable import drawable

class Projectile(drawable):

    def __init__(self,xposition,yposition,velocity = 300,angle = 90,enemies=None,damage=10):
        path = os.path.join("images\Projectiles","riflebullet.png")
        self.dead = False
        self.angle = angle
        self.enemies = enemies
        self.attack = damage
        
        self.shell = False
        self.start = [xposition,yposition]
        self.range =240


        
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
        self.attack = 40
        self.shell = True
        self.range = 360
        
    def travel(self,time):
        oldpos = self.position
        newposy = oldpos.y + self.velocity.y*time.get_time()/1000
        newposx = oldpos.x +self.velocity.x*time.get_time()/1000
        self.position.x = newposx
        self.position.y = newposy

        
            
        if Distance(self.start,list(self.position)) > self.range:
                self.dead = True

        for enemy in self.enemies:
            if self.getCollisionRect().colliderect(enemy.getCollisionRect()):
                enemy.recvDamage(self.attack)
                if not self.shell:
                    self.dead = True
    def die(self):
        self.dead = True

        
    