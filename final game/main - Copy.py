


import pygame
import os
import random
from vector2D import Vector2
from citizen import citizen
from resource import resource
from Queue import queue
from mouse import mouse
from Building import building
from Panel import panel
from drawable import drawable
from ResourceRegister import resourceregister
import testgraph
from testgraph import astar, graphmap
from rifleman import Rifleman
from Cavalry import cavalry
from dummy import Dummy

SCREEN_SIZE = (1200,950)


def main():
   
   # initialize the pygame module
   pygame.init()
   pygame.mixer.init()
   # load and set the logo
   
   
   
   pygame.display.set_caption("The Uncivil Defense")
   
   costregister = {"rifleman":[0,30], "citizen":[0,5], "barracks":[40,0]}
   screen = pygame.display.set_mode(list(SCREEN_SIZE))

   hurt = pygame.mixer.Sound(os.path.join("sound","hurt1.wav"))
   siren = pygame.mixer.Sound(os.path.join("sound","siren.wav"))
   # Let's make a background so we can see if we're moving
   background = pygame.image.load(os.path.join("images", "grass6.jpg")).convert()
   collide = pygame.image.load(os.path.join("images", "citizencollisionrect.png")).convert()
   leftclickpath =os.path.join("images\Tutorial", "leftclick.png")
   rightclickpath = os.path.join("images\Tutorial", "rightclick.png")
   notenoughim = os.path.join("images","Notenough.png")
   leftclick = panel(leftclickpath,leftclickpath,800,400)
   rightclick = panel(rightclickpath,rightclickpath,300,400)
   notenough = panel(notenoughim,notenoughim,700,200)
   mouse1 =os.path.join("images", "mouse.png")
   goldpath = os.path.join("images", "gold.png")
   treepath = os.path.join("images","tree.png")

   panelpath = os.path.join("images", "panel.png")
   buttonpath = os.path.join("images", "citizenbutton.png")
   barrackbuttonpath =os.path.join("images\Buttons", "barracksbutton.png")
   riflemanbuttonpath = os.path.join("images\Buttons", "riflemanbutton.png")


   



   citizenpath = os.path.join("images", "citizen3.png")
   alliedriflepath = os.path.join("images\Rifleman\Walking","180walking1.png")
   dummypath = os.path.join("images\pikeman", "0walking1.png")
   #dummypath = os.path.join("images\Enemies\dummy", "dummy.png")
   #dummy2path = os.path.join(

   homepath =  "testbuilding"
   homepathdir = "images"
   homeselectedpath = "testbuildingse"
   homeselectpathdir = "images"
   barrackdir= "images\Buildings"
   barrackpath = "barracks"
   barrackcollide = pygame.image.load(os.path.join("images", "citizencollisionrect.png")).convert()

   
   home = building(homeselectedpath,homeselectpathdir,homepath,homepathdir,400,390)
  
   barrackselected ="barrackselected"
   

   count = 0
   #testbarrack = drawable(os.path.join("images\Buildings", "barracks" + str(count) + ".png"),800,400)


   position = Vector2(0,0)
   velocity = Vector2(0,0)
   offset = Vector2(0,0)
   #path = os.path.join("images", "sphere1.png")

   cursor = mouse(mouse1)
   point = panel(mouse1,mouse1,0,0)
   uppoint = panel(mouse1,mouse1,0,0)
   downpoint = panel(mouse1,mouse1,0,0)
   rightpoint = panel(mouse1,mouse1,0,0)
   leftpoint = panel(mouse1,mouse1,0,0)
   #Orb = orb(path,velocity,position,offset)
   #Orb.draw()

   citizenlst = []
   selectedcitizen= []
   buildinglst = []
   unbuiltlst = []
   allymilitary= []
   selectedcitizenlst = []
   projectilelst = []
   leftclicklst = [(480,300),(6,622)]
   rightclicklst =[(-400,-400)]

   leftindex = 0
   rightindex = 0

   enemylst = []
   for enemy in enemylst:
      homepos = list(home.getPosition())
      enemy.beginmoving((homepos[0] + 50, homepos[1]+50))
   #Tick the clock
   gameClock = pygame.time.Clock()
   homepos = list(home.getPosition())
   # define a variable to control the main loop
   RUNNING = True

   timer = 0
   
   goldminespot = [(-28,-18), (9,-12),(25,-10)]

   #man = citizen(100,100)
   goldmine = resource(goldpath,600,100,goldminespot)
   tree = resource(treepath,400,100,[(45,70)])


   leftpanel = panel(panelpath,None,0,770)
   rightpanel = panel(panelpath,None,800,770)
   
   button = panel(buttonpath,citizenpath,0,770)
   barrackbutton =  panel(barrackbuttonpath,barrackbuttonpath,0,770)
   riflemanbutton = panel(riflemanbuttonpath,riflemanbuttonpath,0,770)
   touched = False

   
   #barrack = building(barrackselectedpath,barrackpathlst[0],800,390)
   board = graphmap(SCREEN_SIZE)
   register = resourceregister()
   register.addGold(130)
   register.addWood(50)
   blitorder = queue()
   
   
      #rint(enemy.isDead())

   
   timer = 0
   oldtime = 0
   warn = False
   Warnfont =  pygame.font.SysFont("Arial",29)
   warningtxt = Warnfont.render( "WARNING ENEMY APPROACHING",False,(255,0,0) )
   
   finished = True
   displaynotenough =False
   # main loop

   played = False
   while RUNNING:

        
        
        time = int(pygame.time.get_ticks()/1000)

        
        if finished:
           leftclick.position = (-400,-400)
           rightclick.position = (-400,-400)
        else:
         left = min(leftindex,len(leftclicklst)-1)
         right = min(rightindex,len(rightclicklst)-1)
         leftclick.position  = leftclicklst[left]
         rightclick.position = rightclicklst[right]

        if rightindex ==1:
           if abs(righttime-time) > 3:
              rightclicklst.append((-400,-400))
              rightindex +=1
        if rightindex ==2:
            if abs(righttime-time) > 19:
               leftclicklst.append((200,200))
               leftindex+=1

        
        screen.fill((255,255,255))


        if abs(timer -time) > 3 and timer != 0:
           warn = False

        #rint(str(time) + " THis is the timer " + str(timer))
        if (time)%45 ==0 and time != 0:
           timer = time
           warn = True
           if played == False:

            siren.play()
            played = True

         

           
           
           
           
        if (time)%50 ==0 and time != 0 and time != oldtime:
           oldtime = time
           randposx = random.randint(50,80)
           randposy = random.randint(50,80)

           numenemies = random.randint(1,3)
           played = False
           
           

           for i in range (numenemies):
              randposx = random.randint(-10,80)
              randposy = random.randint(-30,50)

              newDummy = Dummy(dummypath,randposx,randposy)
              newDummy.beginmoving((homepos[0] + 50, homepos[1]+50))

              enemylst.append(newDummy)
          



        

        for bullet in projectilelst:
           if bullet.dead ==True:
              projectilelst.remove(bullet)
         #   for enemy in enemylst:
         #      if bullet.getCollisionRect().colliderect(enemy.getCollisionRect()):
         #         enemy.recvDamage(4)
         #         bullet.die()
         #         hurt.play()

      # Draw everything, adjust by offset
        screen.blit(background,list((0,0)))
        if warn == True:
           screen.blit(warningtxt,(800,60))
      
        isbarrackselected = False
        #screen.blit(collide,list(man.position))
        cursor.draw(screen)
        leftpanel.draw(screen)
        leftclick.draw(screen)
        rightclick.draw(screen)
        rightpanel.draw(screen)
        register.draw(screen)

        if displaynotenough:
           if abs(time-notenoughtime)< 5:
            notenough.draw(screen)



        HPfont =  pygame.font.SysFont("Arial",32)
        homehp = HPfont.render( (" Castle Hitpoints :" + str(home.HP)),False,(0,0,0) )
        
        screen.blit(homehp,(470,800))
        button.draw(screen,home.isselected())

        if home.isDead():
           RUNNING = False
        if len(enemylst) > 0:
         for enemy in enemylst:
            
            enemy.shoot(pygame.time,projectilelst,allymilitary)
            enemy.walk(pygame.time)
            enemy.go(gameClock,buildinglst)
            enemy.draw(screen)
            
            if enemy.isDead():
                #rint("remving")
                enemylst.remove(enemy)
            elif enemy.getCollisionRect().colliderect(home.getCollisionRect()):
               home.recvdamage(20)
               enemy.kill()
           
        if len(buildinglst) >0:
           for buildings in buildinglst:
              if buildings.isselected():
                 leftclicklst.append((6,622))
                 leftindex+=1
                 isbarrackselected = True
               
              buildings.changecolliderect((0.5,0.5))
            
              #buildings.drawcollide(screen)
                 

        riflemanbutton.draw(screen,isbarrackselected)

        
        goldmine.draw(screen)
        tree.draw(screen)

        #testbarrack.draw(screen)
        #barrack.draw(screen)
        selectedexists = False
        
        if len(buildinglst)>=1:
         for buildings in buildinglst:
               buildings.draw(screen)
               buildings.update()
        
        if len(allymilitary)>=1:
           #rint(citizenlst)
           for soldier in allymilitary:
              soldier.shoot(pygame.time,projectilelst,enemylst)
              soldier.go(gameClock,buildinglst)
              soldier.walk(pygame.time)
              
              soldier.draw(screen)
              
        for bullet in projectilelst:
           bullet.draw(screen)
           bullet.travel(gameClock)

              
        if len(citizenlst)>=1:
           test = citizenlst[0]
           #rint(citizenlst)
           for citizen in citizenlst:
           
              
              
              citizen.mine(pygame.time,register)
              citizen.chop(pygame.time,register)
              citizen.go(gameClock,buildinglst,citizen.building)
              #citizen.update(citizenlst)
              citizen.walk(pygame.time)
              citizen.draw(screen)
              citizen.build(pygame.time)
              if citizen.isselected():
                 selectedexists = True
      
       
        
      

        for citizen in citizenlst:
           if citizen not in blitorder.orderlst:
              blitorder.adding(citizen)



         
        #rint("selected exists: " + str(isbarrackselected))
        if selectedexists:
           barrackbutton.draw(screen) 
              

             
           
           
        
        home.draw(screen)

        pygame.display.flip()

        
           
         
         
        
        for event in pygame.event.get():
          
              rand = random.randint(0,1)

              if event.type == pygame.KEYDOWN:
                  #tutorial = pygame.image.load(os.path.join("images", "axe1.png")).convert()
                  #screen.blit(tutorial,[500,500])
                  print("============ This is Pos" + str(pygame.mouse.get_pos()))


                  
              if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
               # change the value to False, to exit the main loop
                 RUNNING = False

               

              if event.type == pygame.KEYDOWN:
                 for riflesold in allymilitary:
                    riflesold.goshoot()
               
                 
              
              if event.type == pygame.KEYUP:
                 for riflesold in allymilitary:
                    riflesold.shooting = False
               #   rowlst  = []
               #   for row in board.maze:
               #      for pixel in row:
               #         if pixel ==1:
               #            if board.maze.index(row)  not in rowlst:
               #                #print("THis is row " + str(board.maze.index(row))+ "   " +str(row))
               #                rowlst.append(board.maze.index(row))

               
              if event.type == pygame.MOUSEBUTTONDOWN:
                 
                 if cursor.getCollisionRect().colliderect(leftpanel.getCollisionRect()) == False:
                        cursor.occupied = False
                        home.unselect()
                  
                 for buildings in buildinglst:
                     if cursor.getCollisionRect().colliderect(leftpanel.getCollisionRect()) == False:
                           cursor.occupied = False
                           buildings.unselect()

                 if event.button ==1:
                     if cursor.getCollisionRect().colliderect(button.getCollisionRect()):
                        if home.isselected():

                           newcitizen = home.spawn("citizen",register)

                           
                           if newcitizen in (True,False):
                              displaynotenough = True
                              notenoughtime = time
                              #screen.blit(Noresourcetxt,(800,60))
                           else:
                           
                              randomx = random.randint(-200,-40)
                              randomy= random.randint(-200,-40)

                              leftclicklst.append(tuple((home.getPosition().x+randomx-leftclick.getWidth()+80,home.getPosition().x+randomy-leftclick.getHeight())))
                              leftindex +=1
                              newcitizen.beginmoving(list((home.getPosition().x+randomx,home.getPosition().x+randomy)))
                              citizenlst.append(newcitizen)
                              #rint("This is gold before: "+ str(register.gold))
                              register.addGold(-1*costregister["citizen"][1])
                              #rint("This is gold after: "+ str(register.gold))
                           
                              
                        
                     for buildings in buildinglst:
                        # if cursor.getCollisionRect().colliderect(buildings.getCollisionRect()):
                        #    if cursor.occupied ==False:
                        #       buildings.select()
                        #       cursor.occupied = True
                        if buildings.isselected():
                           if cursor.getCollisionRect().colliderect(riflemanbutton.getCollisionRect()):
                              
                              cav = cavalry("Red",300,400)

                              riflesoldier = buildings.spawn("rifleman",register)
                              finished = True
                              
                              
                              #rint("gold " +str(register.gold))
                              if riflesoldier in (True,False):

                                 displaynotenough = True
                                 notenoughtime = time
                                 pass#rint("++++++++++NO++++++++++++++++++")
                              else:
                              
                                 riflesoldier.quickshootfix()
                                 register.addGold(-1*costregister["rifleman"][1])
                                 randomx = random.randint(-80,-40)
                                 randomy= random.randint(-100,-40)
                                 riflesoldier.beginmoving([randomx+buildings.getPosition().x,randomy + buildings.getPosition().y])
                                 allymilitary.append(riflesoldier)
                                 allymilitary.append(cav)

                                 cav.beginmoving([randomx+buildings.getPosition().x,randomy + buildings.getPosition().y+300])
                           
                        
                           
                     for buildings in buildinglst:
                        if cursor.getCollisionRect().colliderect(buildings.getCollisionRect()):
                           if cursor.occupied ==False:
                              buildings.select()
                              cursor.occupied = True
                     
                     if cursor.getCollisionRect().colliderect(home.getCollisionRect()):
                        if cursor.occupied ==False:
                           home.select()
                           leftindex +=1
                           cursor.occupied = True
                           if len(selectedcitizen) != 0:
                                 selectedcitizen.remove(selectedcitizen[len(selectedcitizen)-1])
                     for man in citizenlst: 
                        if cursor.getCollisionRect().colliderect(man.getCollisionRect()):
                                 #mouse is selecting the human
                                 if cursor.occupied == False:
                                    man.select()
                                    leftclicklst.append((6,622))
                                    leftindex +=1

                                    selectedcitizen.append(man)
                                    
                                    cursor.occupied = True
                     
                        if man.isselected():
                           selectedcitizenlst =[]
                           selectedcitizenlst.append(man)
                           if cursor.getCollisionRect().colliderect(barrackbutton.getCollisionRect()):

                                 leftclicklst.append((-400,-400))
                                 leftindex +=1
                                 barracks = building(barrackselected,barrackdir,barrackpath,barrackdir,300,400,0)
                                 barracks.changecolliderect(barrackcollide)
                                 rightclicklst.append((200,290))

                                 righttime = time

                                 rightindex +=1
                                 register.addWood(-1*costregister["barracks"][0])
                                 unbuiltlst.append(barracks)
                                 

                                 cursor.occupied = True

                     for soldier in allymilitary:
                        if cursor.getCollisionRect().colliderect(soldier.getCollisionRect()):
                                 #mouse is selecting the human
                                 if cursor.occupied == False:
                                    soldier.select()
                                    #selectedcitizen.append(man)
                                    cursor.occupied = True


                        
                 if event.button ==3:
                     if len(unbuiltlst) >=1:
                        tobuild =  unbuiltlst[0]
                        builder = selectedcitizenlst[0]
                        tobuild.position.x = pygame.mouse.get_pos()[0]
                        tobuild.position.y =pygame.mouse.get_pos()[1]-tobuild.getHeight()
                        builder.gobuild(tobuild)
                        builder.beginmoving((tobuild.position.x-20, tobuild.position.y+tobuild.getHeight()-42))
                        
                        buildinglst.append(unbuiltlst[0])
                        
                        
                     for soldier in allymilitary:
                        if soldier.isselected():
                           cursor.occupied = True

                        #IF not in a shooting state:
                           soldier.beginmoving(list(pygame.mouse.get_pos()))
                        else:
                           soldier.unselect()
                           cursor.occupied = False
                           
                     for man in citizenlst:

                     
                        if man.isselected():
                           
                           
                           cursor.occupied = True

                          

                           if cursor.getCollisionRect().colliderect(goldmine.getCollisionRect()):
                              #rint("----------------selected ------------------------")
                              #rint(str(goldmine.occupied))
                              cursor.occupied = True
                              if goldmine.occupied ==False:
                                    #print("i am here")
                                    man.goMine(goldmine)
                                    man.mining = True
                                    goldmine.markandgogather(man)
                              
                           elif not (cursor.getCollisionRect().colliderect(goldmine.getCollisionRect())):
                              
                              man.unmine(goldmine)
                              cursor.occupied = False
                           
                              man.beginmoving(list(pygame.mouse.get_pos()))
                           if cursor.getCollisionRect().colliderect(tree.getCollisionRect()):
                              #print("----------------selected ------------------------")
                              #rint(str(goldmine.occupied))
                              cursor.occupied = True
                              if tree.occupied ==False:
                                    #print("i am here")
                                    man.goChop(tree)
                                    man.chopping= True
                                    tree.markandgogather(man)
                           elif not (cursor.getCollisionRect().colliderect(goldmine.getCollisionRect())):
                              
                              man.unchop(tree)
                              cursor.occupied = False
                              
                        
                                 
                        else:
                              cursor.occupied = False
                              unbuiltlst= []
                              man.unselect()
                              if len(selectedcitizen) != 0:
                                 selectedcitizen.remove(selectedcitizen[len(selectedcitizen)-1])
                        
                              
                    

              
                
                
              
               

        gameClock.tick(60)
        ticks = gameClock.get_time() / 1000

      
      
      
  
      
   pygame.quit()

if __name__ == "__main__":
   main()
   
