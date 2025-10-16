from Physics.vector2D import Vector2
from Physics.physics import Distance,rad
from Physics.drawable import drawable
from Props.Panel import panel
from Actors.character import Character
import os
import pygame
from Physics.projectile import Projectile
import math
from Cinematics.Explosion import *
from Cinematics.Cinematics_manager import *

Bonus = {"Pikeman":-10, "Rifleman":-10,"Building":-30,"Cavalry":-30,"Cannon":-4}

class cannon(Character):
    def __init__(self,color,xposition,yposition):
        if color =="Green":
            self.color = "green"
            path = os.path.join("images\Cannon" +"\Green", "90walking1.png")
            self.angle = 0
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
        self.attack = 40
        self.HP = 130
        self.type = "Cannon"
        self.frame = 2
        self.explosion = False
        self.veradjust = 30

        self.shootsound = pygame.mixer.Sound(os.path.join("sound","cannonshooting.wav"))

        self.direction = "0"
        self.moving = True

        self.rangeimage = os.path.join("images\Cannon","riflerangerect.png")
        self.verimage= os.path.join("images\Cannon","uprange.png")
        self.radarimage = os.path.join("images","radar.png")

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

    def shoot(self, clock, projectilelst, enemylst, ExplosionLst):
        '''
        Handles cannon shooting with explosion effects using dictionary
        '''
        time = clock.get_ticks()/1000
        frame = 9
        distancedict = {}
        sortedenemy = []
        
        self.shootimage = self.image
        self.shooting = False
        
        # Find enemies in range
        for enemy in enemylst:
            xdiff = self.getPosition().x - enemy.getPosition().x
            ydiff = self.getPosition().y - enemy.getPosition().y
            xdiff = min(xdiff, 0.0001)
            angle = (abs(math.atan(ydiff/xdiff)))*180/(math.pi)
            
            for rect in self.rangelst:
                if enemy.getCollisionRect().colliderect(rect.getCollisionRect()):
                    distance = Distance(list(enemy.getPosition()), list(self.getPosition()))
                    self.shooting = True
                    self.going = False
                    self.starttime = 0
                    
                    distancedict[distance] = enemy
                    sortedenemy.append(distance)
        
        start = list(self.position)
        if Distance(start, self.end) - self.tolerance > 36 and not self.shooting:
            self.going = True  
        
        # Handle targeting when not shooting but enemy spotted
        if not self.shooting and not self.going:
            distancedict = {}
            sortedenemy = []
            for enemy in enemylst:
                if enemy.getCollisionRect().colliderect(self.radar.getCollisionRect()):
                    distance = Distance(list(enemy.getPosition()), list(self.getPosition()))
                    distancedict[distance] = enemy
                    sortedenemy.append(distance)
            
            if sortedenemy:
                sortedenemy.sort()
                target = distancedict[sortedenemy[0]]
                xdiff = self.getPosition().x - target.getPosition().x
                ydiff = self.getPosition().y - target.getPosition().y
                
                if xdiff < ydiff:
                    self.end[0] = target.getPosition().x
                else:
                    self.end[1] = target.getPosition().y
        
        # Handle shooting animation and projectile creation
        if self.shooting:
            sortedenemy.sort()
            target = distancedict[sortedenemy[0]]
            
            # Determine shooting direction
            if target.getCollisionRect().colliderect(self.rangeup.getCollisionRect()):
                direction = "0"
                self.angle = 0
            elif target.getCollisionRect().colliderect(self.rangedown.getCollisionRect()):
                direction = "180"
                self.angle = 180
            elif target.getCollisionRect().colliderect(self.rangeleft.getCollisionRect()):
                direction = "270"
                self.angle = 270
            elif target.getCollisionRect().colliderect(self.rangeright.getCollisionRect()):
                direction = "90"
                self.angle = 90
            else:
                direction = "0"
                self.angle = 0
     
            # Load shooting animation
            if self.color == "Red":
                self.shootimage = pygame.image.load(os.path.join("images\Cannon\Red", direction+"shooting"+str(max(1,round(self.shootcursor/frame)))+".png")).convert()
            else:
                self.shootimage = pygame.image.load(os.path.join("images\Cannon\Green", direction+"shooting"+str(max(1,round(self.shootcursor/frame)))+".png")).convert()
            
            self.shootimage.set_colorkey(self.image.get_at((0,0)))
            
            # Update animation
            if abs(time - self.starttime) > 0.01:
                self.changetime(time)
                
                if self.shootcursor > 16 * frame:
                    self.shootcursor = 1
                elif self.shootcursor <= 16 * frame:
                    self.shootcursor += 1
            
            # Create projectile and explosion at the right frame
            if self.shootcursor == 14 * frame:
                # Create cannon explosion effect using dictionary
                self.create_cannon_explosion(direction, ExplosionLst)
                
                # Create projectile
                bullet = self.create_projectile(direction, target, enemylst)
                projectilelst.append(bullet)
                
                # Play sound
                channel = pygame.mixer.find_channel()
                if channel is not None:
                    channel.set_volume(0.8)
                    channel.play(self.shootsound)

    def create_cannon_explosion(self, direction, ExplosionLst):
        '''
        Creates explosion effect at cannon muzzle and stores in dictionary with cannon as key
        '''
        if direction == "90":  # Right
            explosion_x = self.position.x + 192
            explosion_y = self.position.y + 37
            explosion_angle = 0
        elif direction == "180":  # Down
            explosion_x = self.position.x + 90
            explosion_y = self.position.y + 90
            explosion_angle = 90
        elif direction == "0":  # Up
            explosion_x = self.position.x + 90
            explosion_y = self.position.y + 2
            explosion_angle = 270
        elif direction == "270":  # Left
            explosion_x = self.position.x + 60
            explosion_y = self.position.y + 37
            explosion_angle = 270
        else:
            explosion_x = self.position.x + 192
            explosion_y = self.position.y + 92
            explosion_angle = 0
        
        # Create explosion and store in dictionary with cannon as key
        cannon_explosion = Explosion(explosion_x, explosion_y, explosion_angle, 1.5)
        cannon_explosion.duration = 250  # Shorter duration for cannon muzzle flash
        
        # Use cannon object as key in dictionary
        ExplosionLst[self] = cannon_explosion

    def create_projectile(self, direction, target, enemylst):
        '''
        Creates projectile based on shooting direction
        '''
        if direction == "90":  # Right
            bullet = Projectile(self.position.x + 135, self.position.y + 31, 400, int(direction), enemylst)
        elif direction == "180":  # Down
            bullet = Projectile(self.position.x + 86, self.position.y + 89, 400, int(direction), enemylst)
        elif direction == "0":  # Up
            bullet = Projectile(self.position.x - 10 + 0.33 * self.getWidth(), self.position.y - self.getHeight(), 400, int(direction), enemylst)
        elif direction == "270":  # Left
            bullet = Projectile(self.position.x - 10, self.position.y + 10, 400, int(direction), enemylst)
        else:
            bullet = Projectile(self.position.x + 135, self.position.y + 31, 400, 90, enemylst)
        
        bullet.changetocannon()
        bullet.attack = self.attack + Bonus.get(target.type, 0)
        
        return bullet

    # ... rest of your existing methods remain the same ...
    def beginmoving(self, end):
        self.going = True
        self.shooting = False
        self.start = list(self.position)
        self.end = end

    def getCollisionRect(self):
        return self.collideim.getCollisionRect()

    def updaterange(self):
        cpointy = self.position.y + self.centery * self.getHeight()  
        cpointx = self.position.x + self.centerx * self.getWidth() 

        self.radar.position.x = cpointx - self.radar.getWidth() * 0.5
        self.radar.position.y = cpointy - self.radar.getHeight() * 0.5

        self.rangeup.position.x = cpointx - 6
        self.rangeup.position.y = cpointy - 300

        self.rangedown.position.x = cpointx - 6
        self.rangedown.position.y = cpointy + 60

        self.rangeleft.position.x = cpointx - 330
        self.rangeleft.position.y = cpointy - 8

        self.rangeright.position.x = cpointx + 20
        self.rangeright.position.y = cpointy - 12

    def draw(self, surface):
        self.updatecollide()
        self.updaterange()

        if [self.dead, self.shooting, self.going] == [False, False, False]:
            surface.blit(self.image, list(self.position))
            self.image.set_colorkey(self.image.get_at((0,0)))
         
        if self.selected:
            surface.blit(self.selectedim, [self.getPosition().x + 34, self.getPosition().y - 7])
            self.selectedim.set_colorkey(self.selectedim.get_at((0,0)))

        if self.shooting and self.going:
            self.shooting = False
            self.image = self.walkimage
            surface.blit(self.image, list(self.position))
            self.image.set_colorkey(self.image.get_at((0,0)))
        elif self.shooting:
            self.image = self.shootimage
            surface.blit(self.image, list(self.position))
            self.image.set_colorkey(self.image.get_at((0,0)))

        if self.going and not self.shooting:
            self.image = self.walkimage
            surface.blit(self.image, list(self.position))
            self.image.set_colorkey(self.image.get_at((0,0)))

    def walk(self, clock, framerate=5):
        frame = framerate
        maxframe = 4
        time = clock.get_ticks() / 28

        if self.going:
            direction = self.getAnglestate()
            self.direction = direction

            if self.getAnglestate() not in ("270", "180", "90", "0"):
                direction = "0"
                self.direction = direction
            
            if self.color == "Red":
                self.walkimage = pygame.image.load(os.path.join("images\Cannon\Red", direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()
            else:
                self.walkimage = pygame.image.load(os.path.join("images\Cannon\Green", direction+"walking"+str(max(1,round(self.cursor/frame)))+".png")).convert()

            self.walkimage.set_colorkey(self.image.get_at((0,0)))
            
            if (time - self.starttime > 0.7):
                self.changetime(time)
                
                if self.cursor > maxframe * frame:
                    self.cursor = 1
                
                if self.cursor <= maxframe * frame:
                    self.cursor += 1
                
                if self.cursor > maxframe * frame:
                    self.cursor = 1
        else:
            self.image = self.imageres

    def updatecollide(self):
        cpointy = self.position.y + self.centery * self.getHeight() + 19
        cpointx = self.position.x + self.centerx * self.getWidth() - 8

        self.collideim.position.x = cpointx - 30
        self.collideim.position.y = cpointy - self.veradjust