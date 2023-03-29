

from doctest import register_optionflag
from sqlite3 import SQLITE_CREATE_INDEX


from Check import check
import pygame
import os
import random
from pikeman import Pikeman
from Gamemanager import Mode
from vector2D import Vector2
from citizen import Citizen
from resource import resource
from Queue import queue
from mouse import mouse
from Building import building
from Panel import panel
from drawable import drawable
from ResourceRegister import resourceregister
from testgraph import astar, graphmap
from rifleman import Rifleman
from Cavalry import cavalry
from Cannon import cannon
from dummy import Dummy
from paths import*


SCREEN_SIZE = (1440,900)


def main(cond=None):



   
   
      # initialize the pygame module
   pygame.init()
   pygame.mixer.pre_init()
   pygame.mixer.init()
   pygame.mixer.set_num_channels(1000)
   # load and set the logo
   
   
   
   pygame.display.set_caption("The Uncivil Defense")
   
   costregister = {"rifleman":[0,30], "citizen":[0,5], "barracks":[40,0],"tower":[50,0],"pikeman":[10,5],"cavalry":[0,60],"cannon":[100,200]}
   #screen = pygame.display.set_mode(list(SCREEN_SIZE),pygame.FULLSCREEN) #SET TO FULL SCREEN
   screen = pygame.display.set_mode(list(SCREEN_SIZE))

   hurt3 = pygame.mixer.Sound(os.path.join("sound","hurt3.wav"))
   hurt4 = pygame.mixer.Sound(os.path.join("sound","hurt4.wav"))
   
   hurtlst=[hurt4,hurt3]
   siren = pygame.mixer.Sound(os.path.join("sound","siren.wav"))
   # Let's make a background so we can see if we're moving
   background = pygame.image.load(os.path.join("images", "grass6.jpg")).convert()
   scroll = pygame.image.load(os.path.join("images\Menu", "menu1.png")).convert()


   collide = pygame.image.load(os.path.join("images", "citizencollisionrect.png")).convert()

   leftclickpath =os.path.join("images\Tutorial", "leftclick.png")
   rightclickpath = os.path.join("images\Tutorial", "rightclick.png")
   notenoughim = os.path.join("images","Notenough.png")





   leftclick = panel(leftclickpath,leftclickpath,800,400)
   rightclick = panel(rightclickpath,rightclickpath,300,400)
   notenough = panel(notenoughim,notenoughim,874,308)

   selectedbuttons = [easy1path,medium1path,hard1path,tutorial1path,quit1path]
   unselectedbuttons =[easypath,mediumpath,hardpath,tutorialpath,quitpath]



   alliedriflepath = os.path.join("images\Rifleman\Walking","180walking1.png")
   #dummypath = os.path.join("images\pikeman", "0walking1.png")
   dummypath = os.path.join("images\Enemies\dummy", "dummy.png")
   #dummy2path = os.path.join(

   homepath =  "testbuilding"
   homepathdir = "images"
   homeselectedpath = "testbuildingse"
   homeselectpathdir = "images"

   barrackdir= "images\Buildings"
   barrackpath = "barracks"
   barrackcollide = pygame.image.load(os.path.join("images", "citizencollisionrect.png")).convert()

   towerdir = barrackdir
   towerpath = "tower"
   towercollide = barrackcollide
   towerselected = "towerselected"
   
   home = building(homeselectedpath,homeselectpathdir,homepath,homepathdir,520,300)
   home.ishome = True
   pole = drawable(flagpolepath,home.position.x+60,home.position.y)
   flag1 = drawable(flag1path,home.position.x+74,pole.position.y)
   flag2 = drawable(flag2path,home.position.x+74,home.position.y+pole.getHeight())

   
   barrackselected ="barrackselected"

   cursor = mouse(mouse1)

   allymilitary =[Pikeman("Red",random.randint(200,300),100) for x in range(10)]

   resourcelst= []
   citizenlst = []
   selectedcitizen= []
   buildinglst = [home]
   buildinglst[0].maxprogress = ''
   unbuiltlst = []
   allymilitary= []
   selectedcitizenlst = []
   flamelst = []

   projectilelst = []

   Allbuildings = [buildinglst,[home],resourcelst]


   leftclicklst = [(590,250),(6,622)]
   rightclicklst =[(-400,-400)]

   leftindex = 0
   rightindex = 0

   enemylst = []
   
   homepos = list(home.getPosition())

   #Tick the clock
   gameClock = pygame.time.Clock()
   homepos = list(home.getPosition())

   timer = 0

   goldpos = [600,100]

   treeminespot = [45,70]
   treepos = [400,100]


   easylst = [540,100]
   easy = drawable(easypath,easylst[0],easylst[1])
   medium = drawable(mediumpath,easylst[0]+10,easylst[1]+160)
   hard = drawable(hardpath,easylst[0]-17,easylst[1]+300)
   tutorial = drawable(tutorialpath,easylst[0]-17,easylst[1]+470)
   quit = drawable(quitpath,easylst[0]+400,easylst[1]+590)
   restart = drawable(restartpath,600,700 )
   loseimage = drawable(losepath,0,0)
   victoryimage = drawable(victorypath,0,0)

   if cond ==None:

      for i in range(10):
         
         randy = random.randint(-90,120)
         randx = i*60
         grandx = 350 + i*45
         grandy = 400+random.randint(-90,120)
         goldminespot = [(-28+grandx,-1+grandy), (9+grandx,-1+grandy),(25+grandx,-1+grandy)]
         goldmine = resource(goldpath,600+grandx,100+grandy,goldminespot,"mine")
         tree = resource(treepath,400+randx,100+randy,[(30+randx,70+randy)],"tree")

         resourcelst.append(goldmine)
         
            
         resourcelst.append(tree)

      toberemoved = []


      
      for index in toberemoved:
         resourcelst[index] = 'r'

      for item in resourcelst:
         if item =='r':
            resourcelst.remove(item)


      leftpanel = panel(panelpath,None,0,700)
      rightpanel = panel(rightpanelpath,None,830,700)
      timepanel = drawable(timerpath,470,686)





      buttonlst = [easy,medium,hard,tutorial,quit]
      mode1 = Mode("easy")
      mode2 = Mode("medium")
      mode3 = Mode("hard")
      mode4 = Mode("tutorial")
      mode5 = Mode("quit")




      conditionlst = [mode1,mode2,mode3,mode4,mode5]
      global quill  
      quill = drawable(quillpath,0,0)
      
      button = panel(buttonpath,citizenpath,0,745)
      barrackbutton =  panel(barrackbuttonpath,barrackbuttonpath,0,745)
      towerbutton =  panel(towerbuttonpath,towerbuttonpath,170,745)
      
      riflemanbutton = panel(riflemanbuttonpath,riflemanbuttonpath,0,745)
   
      cannonbutton = panel(cannonbuttonpath,cannonbuttonpath,170,745)
      cavalrybutton = panel(cavalrybuttonpath,cavalrybuttonpath,0,745)
      pikemanbutton = panel(pikemanbuttonpath,pikemanbuttonpath,170,745)
      

      touched = False
      board = graphmap(SCREEN_SIZE)
      register = resourceregister()
      register.addGold(500)
      register.addWood(120)
      blitorder = queue()
      Checker = check()
      
      
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

      Menu = True


      easyimage = pygame.image.load(easypath)
      while Menu:


         screen.fill((255,255,255))
         screen.blit(scroll,list((0,0)))
         
         
         for buttons in buttonlst:
            buttons.image.set_colorkey(buttons.image.get_at((0,0)))
         

            buttons.draw(screen)
         mousepos = pygame.mouse.get_pos()

         quill.position.x = mousepos[0]
         quill.position.y = mousepos[1]-quill.getHeight()
         quill.draw(screen)

         #pygame.draw.rect(screen,(0,0,255),easy.getCollisionRect())  
         for buttons in buttonlst:
            if buttons.getCollisionRect().collidepoint(mousepos[0],mousepos[1]):
               buttons.image = pygame.image.load(selectedbuttons[buttonlst.index(buttons)])
               

               
            else:
               buttons.image = pygame.image.load(unselectedbuttons[buttonlst.index(buttons)])

         

         for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:


               if event.button == 1:

                  for buttons in buttonlst:


                     if buttons.getCollisionRect().collidepoint(mousepos[0],mousepos[1]):


                        Menu = False
                        mode = conditionlst[buttonlst.index(buttons)].getMode()
                        
         
         
         pygame.display.flip()

      RUNNING = True
      win = False
      lose = False

      cannonlimit = 15
      scale = 1
      gold = 100
      Wood = 100
   
      interval =30
      if mode =="tutorial":
         finished = False
         interval =60
         winminute = 3.3
         rate = 0.2
      if mode =="easy":
         scale =5
         interval = 50
         winminute = 5
         rate = 2

      if mode =="medium":
         scale = 3
         interval = 45
         winminute = 8
         rate = 6
      if mode == "hard":
         interval = 30
         winminute =10
         rate = 8
      else:
         winminute = 3.3


      
      gold*=scale
      Wood*= scale
      goldingot = drawable(goldingotpath,950,785)
      woodingot = drawable(woodingotpath,1180,785)

      register.gold = gold
      register.wood = Wood

      wintime = 60*(winminute)


      gamestart = int(pygame.time.get_ticks()/1000)
      oldtime = gamestart
      grade= 3
      flagrate = pole.getHeight()/home.HP

      

      while RUNNING and mode != "quit":

         #Tutorial
         screen.fill((255,255,255))
         time = int(pygame.time.get_ticks()/1000)

         ychange = home.HP*flagrate


         flag1.position.y = pole.position.y -ychange+93
         flag2.position.y = home.position.y+pole.getHeight()+ychange-93



         
         if finished:
            leftclick.position = (-400,-400)
            rightclick.position = (-400,-400)
         else:

            #move to the next tutorial cursor
            left = min(leftindex,len(leftclicklst)-1)
            right = min(rightindex,len(rightclicklst)-1)
            leftclick.position  = leftclicklst[left]
            rightclick.position = rightclicklst[right]

         #just skip the first two right indices 
         if rightindex ==1:
            if abs(righttime-time) > 3:
               rightclicklst.append((-400,-400))
               rightindex +=1
         if rightindex ==2:
               if abs(righttime-time) > 19:
                  leftclicklst.append((200,200))
                  leftindex+=1
         
         

         if abs((time-gamestart))>wintime:
            win = True
            RUNNING = False
            main("w")

         

         if abs(timer -time) > 3 and timer != 0:
            warn = False

         #rint(str(time) + " THis is the timer " + str(timer))
         if abs(oldtime-time) > (interval-5):
         #if (time)%30 ==0 and time != 0:
            
            warn = True
            timer = time
            if played == False:

               siren.play()
               played = True
            
         if abs(oldtime-time) > interval:
            #print(" This is time " + str(time) +" This is diff " + str(oldtime-time) + " THis is grade " + str(grade) + ' rate ' + str(rate))
         #if (time)%36 ==0 and time != 0 and time != oldtime:
            oldtime = time
            if 1 == random.randint(0,3):
               grade += rate
            cannonlimit -= rate

            temp = cannonlimit
            cannonlimit  = round(max(1,cannonlimit))

            randposx = random.randint(50,80)
            randposy = random.randint(50,80)

            numenemies = random.randint(1,round(grade))
            
            played = False
            
            cannondie = random.randint(1,max(2,cannonlimit))
            direction = 0
            

            if direction  == 0:
               xchange = 0
               ychange = 31
               randposx = random.randint(20,58)
               randposy = random.randint(93,180)

   
               
               #invade eastwards
            for i in range (numenemies):
                     
                     
                     riflesold = Rifleman(riflepath,randposx-30,randposy+i*(ychange))
                     spearman = Pikeman("Red",randposx+10,randposy+i*(ychange))
                     if random.randint(1,5) == 1:
                        artillery = cannon("Red",randposx-5,randposy+i*(ychange))
                        artillery.beginmoving((260+i*(round(xchange)), 350+i*round(ychange)))
                        

                        enemylst.append(artillery)
                        cav = cavalry("Red",randposx+20+i*(xchange),randposy+i*(ychange))
                        cav.beginmoving((280+i*(round(xchange)), 330+i*(round(ychange/0.8))))
                        enemylst.append(cav)

                     riflesold.quickshootfix("Red")
                     riflesold.beginmoving((280, 430+ i*(ychange)))

                     spearman.beginmoving((280+ i*(round(xchange)), 400+ i*ychange))


                     enemylst.append(riflesold)
                     enemylst.append(spearman)
               



         

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
            screen.blit(warningtxt,(874,308))
         
         isbarrackselected = False
         istowerselected = False
         #screen.blit(collide,list(man.position))
         cursor.draw(screen)
         leftpanel.draw(screen)
         leftclick.draw(screen)
         rightclick.draw(screen)
         rightpanel.draw(screen)
         timepanel.draw(screen)
         #register.draw(screen)
         
         text = pygame.font.SysFont("Arial",23)

         
         goldtxt = text.render( (  str(round(gold))),False,(0,0,0))

         Woodtxt = text.render( (str(round(Wood))),False,(0,0,0))
                  
         screen.blit(goldtxt,(1044,799))

         screen.blit(Woodtxt,(1278,804))

         goldingot.draw(screen)
         woodingot.draw(screen)

         if displaynotenough:
            if abs(time-notenoughtime)< 5:
               notenough.draw(screen)



         HPfont =  pygame.font.SysFont("Arial",22)
         homehp = HPfont.render( str((wintime-time)) + "  Seconds",False,(0,0,0) )
         
         screen.blit(homehp,(610,820))
         button.draw(screen,home.isselected())

         if home.isDead():
            lose = True

            main("lose")
            RUNNING = False
            
            
   
            
         if len(buildinglst) >0:
            for buildings in buildinglst:
               if buildings.isselected() and buildings.maxprogress==5:
                  leftclicklst.append((6,622))
                  leftindex+=1
                  isbarrackselected = True
               if buildings.isselected() and buildings.maxprogress==9:
                  istowerselected = True

                  
               buildings.changecolliderect((0.5,0.5))
               
               #buildings.drawcollide(screen)
         if home.HP < 500 and home.HP%50 == 0:
            randx = random.randint(home.position.x+30,home.position.x+home.getWidth()-20)
            randy = random.randint(home.position.y+30,home.position.y+home.getHeight()-20)
            flame = drawable(flamepath,randx,randy)
            home.HP -=1
            flamelst.append(flame)



         
         
         
         riflemanbutton.image.set_colorkey(riflemanbutton.image.get_at((0,0)))
         
         riflemanbutton.draw(screen,isbarrackselected)



         pikemanbutton.draw(screen,isbarrackselected)
         pikemanbutton.image.set_colorkey(riflemanbutton.image.get_at((0,0)))
         

         cavalrybutton.draw(screen,istowerselected)
         cannonbutton.draw(screen,istowerselected)

         for gatherable in resourcelst:
            
            #pygame.draw.rect(screen,(0,255,00),gatherable.getCollisionRect())
            gatherable.draw(screen)
            # goldmine.draw(screen)
            # tree.draw(screen)

         #testbarrack.draw(screen)
         #barrack.draw(screen)
         selectedexists = False
         
         pole.draw(screen)
         flag1.draw(screen)
         flag2.draw(screen)
         if len(unbuiltlst)>=1:
            for buildings in unbuiltlst:
                  
                  suitable = Checker.checkcollide(cursor,Allbuildings,buildings)
                  if buildings.maxprogress ==5:
                     buildings.drawblueprint(screen,suitable,"barrack")
                  else:
                     buildings.drawblueprint(screen,suitable,"tower")


                  
         
         if len(buildinglst)>=1:
            for buildings in buildinglst:
                  buildings.draw(screen)
                  buildings.update()

         if len(enemylst) > 0:
            for enemy in enemylst:
               
               fullenemies = [item for item in allymilitary]
               fullenemies.append(home)
               enemy.shoot(pygame.time,projectilelst,fullenemies,time)
               enemy.go(gameClock,buildinglst)
               enemy.walk(pygame.time)
               
               enemy.draw(screen)
               
               
               if enemy.isDead():
                  #rint("remving")
                  

                  deathsound = hurtlst[random.randint(0,len(hurtlst)-1)]
                  deathsound.set_volume(0.09)
                  deathsound.play()
                  enemylst.remove(enemy)
                  

         if len(flamelst) > 0:
            for fire in flamelst:
               fire.draw(screen)
         
         if len(allymilitary)>=1:
            #rint(citizenlst)
            for soldier in allymilitary:
               soldier.shoot(pygame.time,projectilelst,enemylst,time)
               soldier.go(gameClock,buildinglst)
               soldier.walk(pygame.time)
               
               soldier.draw(screen)
               if soldier.dead == True:
                  deathsound = hurtlst[random.randint(0,len(hurtlst)-1)]
                  deathsound.set_volume(0.09)
                  deathsound.play()
                  allymilitary.remove(soldier)
               
         for bullet in projectilelst:
            bullet.draw(screen)
            bullet.travel(gameClock)

               
         if len(citizenlst)>=1:
            test = citizenlst[0]
            #rint(citizenlst)
            for citizen in citizenlst:
            
               
               
               citizen.mine(pygame.time,gold)
               if citizen.mining and citizen.arrived == True:
                  gold += citizen.miningrate
               citizen.chop(pygame.time,Wood)
               if citizen.chopping and citizen.arrived == True:
                  Wood += citizen.choppingrate
               
               citizen.go(gameClock,buildinglst,citizen.building)
               #citizen.update(citizenlst)
               citizen.walk(pygame.time)
               citizen.draw(screen)
               citizen.build(pygame.time)
               if citizen.isselected():
                  selectedexists = True
                  towerbutton.draw(screen)
         
         
         
         

         for citizen in citizenlst:
            if citizen not in blitorder.orderlst:
               blitorder.adding(citizen)



            
         #rint("selected exists: " + str(isbarrackselected))
         if selectedexists:
            barrackbutton.draw(screen) 
               

               
            
            
         
         #home.draw(screen)

         pygame.display.flip()

         

         
            
         
            
         
         for event in pygame.event.get():
            
               rand = random.randint(0,1)

               #   if event.type == pygame.KEYDOWN:
               #       #tutorial = pygame.image.load(os.path.join("images", "axe1.png")).convert()
               #       #screen.blit(tutorial,[500,500])
                     


                     
               if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                  # change the value to False, to exit the main loop
                  RUNNING = False

                  
                  
               #   if event.type == pygame.KEYDOWN:
               #      for riflesold in allymilitary:
               #         riflesold.goshoot()
                  
                  
               
               if event.type == pygame.KEYUP:
                  print("============ This is Pos" + str(pygame.mouse.get_pos()))
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
                        if cursor.getCollisionRect().colliderect(leftpanel.getCollisionRect()) == False and buildings.maxprogress != '':
                              cursor.occupied = False
                              buildings.unselect()

                  if event.button ==1:

                     #**********************LEFT CLICK ATIONS *****************************************************

                        for soldier in allymilitary:
                           if cursor.getCollisionRect().colliderect(soldier.getCollisionRect()):
                                    #mouse is selecting the human
                                    if cursor.occupied == False:
                                       soldier.select()
                                       
                                       #selectedcitizen.append(man)
                                       soldier.shooting ==False
                                       cursor.occupied = True

                        if cursor.getCollisionRect().colliderect(button.getCollisionRect()):
                           if home.isselected():


                              newcitizen = home.spawn("citizen",register)

                              newcitizen =Citizen(home.position.x-10, home.position.y-10)

                              if (gold -costregister["citizen"][1]) > 0:
                                 randomx = random.randint(-80,-39)
                                 randomy= random.randint(-170,-110)

                                 leftclicklst.append((newcitizen.getPosition().x,newcitizen.getPosition().y))
                                 leftindex +=1
                                 leftclick.position = (newcitizen.getPosition().x,newcitizen.getPosition().y)
                                 
                                 newcitizen.beginmoving(list((home.getPosition().x+randomx,home.getPosition().x+randomy)))
                                 citizenlst.append(newcitizen)
                                 gold -= costregister["citizen"][1]
                              else:

                              
                                 displaynotenough = True
                                 notenoughtime = time
                                 #screen.blit(Noresourcetxt,(800,60))
                              
                              
   

                                 #rint("This is gold before: "+ str(register.gold))
                                 #register.addGold(-1*costregister["citizen"][1])
                                 #rint("This is gold after: "+ str(register.gold))
                              
                                 
                           
                        for buildings in buildinglst:
                           # if cursor.getCollisionRect().colliderect(buildings.getCollisionRect()):
                           #    if cursor.occupied ==False:
                           #       buildings.select()
                           #       cursor.occupied = True


                           
                           if buildings.isselected() and buildings != buildinglst[0] and buildings:
                              
                              if cursor.getCollisionRect().colliderect(riflemanbutton.getCollisionRect()) and buildings.maxprogress == 5:
                                 
                                 riflepath1 = os.path.join("images\Rifleman\Green\Walking","180walking1.png")
                                 riflesoldier = Rifleman(riflepath1,buildings.position.x+100, buildings.position.y+100)

                                 #finished tutorial
                                 finished = True
                                 
                                 
                                 #rint("gold " +str(register.gold))
                                 if (gold -costregister["rifleman"][1]) >0: # the soldier becomes a boolean if there are not enough resources


                                    riflesoldier.quickshootfix("Green")
                                    gold -= costregister["rifleman"][1]
                                    
                                    randomx = random.randint(100,220)
                                    randomy= random.randint(100,220)
                                    riflesoldier.beginmoving([randomx+buildings.getPosition().x,randomy + buildings.getPosition().y])
                                    allymilitary.append(riflesoldier)
                                    pass#rint("++++++++++NO++++++++++++++++++")
                                 else:
                                    displaynotenough = True
                                    notenoughtime = time
                                 

                                    #allymilitary.append(cav)

                                    #cav.beginmoving([randomx+buildings.getPosition().x,randomy + buildings.getPosition().y+300])

                              if cursor.getCollisionRect().colliderect(pikemanbutton.getCollisionRect()) and buildings.maxprogress == 5:
                                 
                              
                                 spearman = Pikeman("Green",buildings.position.x +100,buildings.position.y+100)
                                 #finished tutorial
                                 
                                 
                                 
                                 #rint("gold " +str(register.gold))
                                 if(gold -costregister["pikeman"][1]) >0 and (Wood -costregister["pikeman"][0]):# the soldier becomes a boolean if there are not enough resources

                                    register.addGold(-1*costregister["pikeman"][1])
                                    register.addWood(-1*costregister["pikeman"][0])

                                    gold += -1*costregister["pikeman"][1]
                                    Wood += -1*costregister["pikeman"][0]

                                    randomx = random.randint(100,220)
                                    randomy= random.randint(100,220)
                                    spearman.beginmoving([randomx+buildings.getPosition().x,randomy + buildings.getPosition().y])
                           
                                    allymilitary.append(spearman)
                                    
                                 else:
                                    displaynotenough = True
                                    notenoughtime = time


                                 
                                 



                           if buildings.isselected() and buildings.maxprogress == 9:
                              if cursor.getCollisionRect().colliderect(cavalrybutton.getCollisionRect()):
                                 
                              
                                 cav = cavalry("Green",buildings.position.x +100,buildings.position.y+100)
                                 #finished tutorial
                                 
                                 
                                 
                                 #rint("gold " +str(register.gold))
                                 if(gold -costregister["cavalry"][1]) >0:# the soldier becomes a boolean if there are not enough resources

                                    

                                    randomx = random.randint(100,220)
                                    randomy= random.randint(100,220)
                                    cav.beginmoving([randomx+buildings.getPosition().x,randomy + buildings.getPosition().y])
                                    gold += -1*costregister["cavalry"][1]
                                    allymilitary.append(cav)
                                    
                                 else:
                                    displaynotenough = True
                                    notenoughtime = time
                              if cursor.getCollisionRect().colliderect(cannonbutton.getCollisionRect()):
                                 
                                 bombard = cannon("Green",buildings.position.x +100,buildings.position.y+100)
                                 #finished tutorial
                                 
                                 
                                 
                                 #rint("gold " +str(register.gold))
                                 if gold -costregister["cannon"][1]> 0 and (Wood -costregister["cannon"][0]) > 0:# the soldier becomes a boolean if there are not enough resources

                                    # register.addGold(-1*costregister["pikeman"][1])
                                    # register.addWood(-1*costregister["pikeman"][0])

                                    randomx = random.randint(100,220)
                                    randomy= random.randint(100,220)

                                    
                                    bombard.beginmoving([randomx+buildings.getPosition().x,randomy + buildings.getPosition().y])

                                    gold += -1*costregister["cannon"][1]
                                    Wood += -1*costregister["cannon"][0]
                           
                                    allymilitary.append(bombard)
                                    
                                 else:
                                    displaynotenough = True
                                    notenoughtime = time
                              
                                 
                                 #finished tutorial
                                 
                                 
                  
                              

                                    

                              
                              
                        for man in citizenlst: 
                           if cursor.getCollisionRect().colliderect(man.getCollisionRect()):
                                    #mouse is selecting the human
                                    if cursor.occupied == False:
                                       man.select()
                                       leftclicklst.append((6,622))
                                       leftindex +=1

                                       selectedcitizen.append(man)
                                       
                                       cursor.occupied = True   
                              
                        for buildings in buildinglst:
                           if cursor.getCollisionRect().colliderect(buildings.getCollisionRect()):
                              if cursor.occupied ==False:
                                 buildings.select()
                                 cursor.occupied = True
                                 if buildinglst.index(buildings) == 0:
                                    leftclicklst.append((50,630))
                                    leftindex+=1
                        
                        if cursor.getCollisionRect().colliderect(home.getCollisionRect()):
                           if cursor.occupied ==False:
                              home.select()
                              leftindex +=1
                              cursor.occupied = True
                              if len(selectedcitizen) != 0:
                                    selectedcitizen.remove(selectedcitizen[len(selectedcitizen)-1])

                        for man in citizenlst:

                           if man.isselected():
                              selectedcitizenlst =[]
                              selectedcitizenlst.append(man)
                              
                              if cursor.getCollisionRect().colliderect(towerbutton.getCollisionRect()):
                                 tower = building(towerselected,towerdir,towerpath,towerdir,300,400,0)
                                 tower.changecolliderect(barrackcollide)
                                 tower.maxprogress =9

                                 register.addWood(-1*costregister["barracks"][0])  
                                 unbuiltlst.append(tower)

                                 

                                 
                                    


                           
                           

                              #if the citizen is about to build a barracks
                              if cursor.getCollisionRect().colliderect(barrackbutton.getCollisionRect()):
                                    
                                    leftclicklst.append((-400,-400))
                                    leftindex +=1   # move tutorial point
                                    barracks = building(barrackselected,barrackdir,barrackpath,barrackdir,300,400,0)
                                    barracks.changecolliderect(barrackcollide)
                                    rightclicklst.append((200,290))

                                    righttime = time  #timer for tutorial arrow

                                    rightindex +=1
                                    register.addWood(-1*costregister["barracks"][0])  
                                    unbuiltlst.append(barracks)
                                    

                                    cursor.occupied = True





                  # LEFT CLICK TRIGGERS
                  #     
                  if event.button ==3:

                     #***************right click methods
                        if len(unbuiltlst) >=1:
                           tobuild =  unbuiltlst[0]

                           x = pygame.mouse.get_pos()[0]
                           y = pygame.mouse.get_pos()[1]+tobuild.getHeight()
                           

                           if Checker.checkcollide(cursor,Allbuildings,tobuild,x,y):


                              

                              builder = selectedcitizenlst[0]
                              tobuild.position.x = pygame.mouse.get_pos()[0]
                              tobuild.position.y =pygame.mouse.get_pos()[1]-tobuild.getHeight()
                              builder.gobuild(tobuild)
                              builder.beginmoving((tobuild.position.x-20, tobuild.position.y+tobuild.getHeight()-42))
                              
                              
                              buildinglst.append(unbuiltlst[0])
                              unbuiltlst.remove(tobuild)
                           
                           
                        for soldier in allymilitary:
                           if soldier.isselected():
                              cursor.occupied = True

                           #IF not in a shooting state:
                              soldier.shooting = False

                              soldier.moving = True
                              
                              soldier.beginmoving(list(pygame.mouse.get_pos()))
                              soldier.unselect()
                           else:
                              soldier.unselect()
                              cursor.occupied = False
                              
                        for man in citizenlst:

                        
                           if man.isselected():

                              man.unchop()
                              man.unmine()
                              
                              
                              
                              cursor.occupied = True

                              
                              for gatherable in resourcelst:

                                 if cursor.getCollisionRect().colliderect(gatherable.getCollisionRect()) and gatherable.kind == "mine":
                                    #rint("----------------selected ------------------------")
                                    #rint(str(goldmine.occupied))
                                    cursor.occupied = True
                                    if gatherable.occupied ==False:
                                          #print("i am here")
                                          man.goMine(gatherable)
                                          man.mining = True
                                          gatherable.markandgogather(man)
                                    
                                 # elif not (cursor.getCollisionRect().colliderect(gatherable.getCollisionRect())):
                                    
                                 #    man.unmine(gatherable)
                                 #    cursor.occupied = False
                              
                              man.beginmoving(list(pygame.mouse.get_pos()))
                              #man.chopping = False
                              #man.mining = False
                              for gatherable in resourcelst:

                                 if cursor.getCollisionRect().colliderect(gatherable.getCollisionRect()) and gatherable.kind == "tree":
                                    #print("----------------selected ------------------------")
                                    #rint(str(goldmine.occupied))
                                    cursor.occupied = True
                                    if gatherable.occupied ==False:
                                          #print("i am here")
                                          man.goChop(gatherable)
                                          man.chopping= True
                                          tree.markandgogather(man)
                                 # elif not (cursor.getCollisionRect().colliderect(gatherable.getCollisionRect())):
                                    
                                 #    man.unchop()
                                 #    cursor.occupied = False
                                 
                           
                                    
                           else:
                                 cursor.occupied = False
                                 unbuiltlst= []
                                 man.unselect()
                                 if len(selectedcitizen) != 0:
                                    selectedcitizen.remove(selectedcitizen[len(selectedcitizen)-1])
                           
                                 
      


               
                  
                  
               
                  

         gameClock.tick(60)
         ticks = gameClock.get_time() / 1000
      
      
      
      print("win  ", win, "lose ", lose)

   if cond == "w":


      print("hereeee ====")
      #winsound.play()
      quill = drawable(quillpath,0,0)
      w= True
      while w:
      
        # screen.fill((255,0,255))
         print("winning")
         screen.blit(victoryimage.image,list((0,0)))
      

         quit.image.set_colorkey(quit.image.get_at((0,0)))
         quit.draw(screen)

         restart.image.set_colorkey(restart.image.get_at((0,0)))
         restart.draw(screen)
         mousepos = pygame.mouse.get_pos()

         quill.position.x = mousepos[0]
         quill.position.y = mousepos[1]-quill.getHeight()
         quill.draw(screen)


         

         for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:


               if event.button == 1:

                  for buttons in buttonls:


                     if quit.getCollisionRect().collidepoint(mousepos[0],mousepos[1]):
                        w ==False
                        #winsound.stop()
                        main()
                     elif restart.getCollisionRect().collidepoint(mousepos[0],mousepos[1]):
                        w= False
                        #winsound.stop()
                        main()

      
      



   else:
      lose = True

      #losesound.play()
      buttonls = [quit,restart]
      while lose:
      
         screen.fill((255,255,255))
         screen.blit(loseimage.image,list((0,0)))
      

         quit.image.set_colorkey(quit.image.get_at((0,0)))
         quit.draw(screen)

         restart.image.set_colorkey(restart.image.get_at((0,0)))
         restart.draw(screen)
         mousepos = pygame.mouse.get_pos()

         quill.position.x = mousepos[0]
         quill.position.y = mousepos[1]-quill.getHeight()
         quill.draw(screen)


         

         for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:


               if event.button == 1:

                  for buttons in buttonls:


                     if quit.getCollisionRect().collidepoint(mousepos[0],mousepos[1]):
                        lose ==False
                        #losesound.stop()
                     elif restart.getCollisionRect().collidepoint(mousepos[0],mousepos[1]):
                        lose == False
                        #losesound.stop()
                        main()


                        
                        
         

         




      
      
      
  
      
   pygame.quit()

if __name__ == "__main__":
   main()
   
