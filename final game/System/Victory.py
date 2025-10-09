
import pygame
import os
import random
from Physics.drawable import drawable
from System.paths import*
victorypath  = os.path.join("images\Menu", "victorypath.png")
losepath = os.path.join("images\Menu", "losepath.png")

SCREEN_SIZE = (1440,900)
#0 is win, 1 is lose
def Win(cond):

   #print("this is cond " + str(cond))
   
   # initialize the pygame module
   pygame.init()

   backgroundls = [victorypath,losepath]
   # load and set the logo
   
   pygame.display.set_caption("Camera")
   
   screen = pygame.display.set_mode(list(SCREEN_SIZE))

   
   # Let's make a background so we can see if we're moving
   background = pygame.image.load(os.path.join("images", "background.png")).convert()
   
   #intialize necessary vectors,paths for movement of orb and screen

   path = os.path.join("images", "sphere1.png")
   #Orb = orb(path,velocity,position,offset)
  # Orb.draw()

   winsound = pygame.mixer.Sound(os.path.join("sound","winsound.wav"))
   losesound = pygame.mixer.Sound(os.path.join("sound","losesound.wav"))
   soundls = [winsound,losesound]
   quit = drawable(quitpath,1161,733)

      
   victoryimage = drawable(backgroundls[cond],0,0)
   quill = drawable(quillpath,0,0)
   #Tick the clock
   gameClock = pygame.time.Clock()
   
   # define a variable to control the main loop
   RUNNING = True

   touched = False


   selectedbuttons = [easy1path,medium1path,hard1path,tutorial1path,quit1path]
   unselectedbuttons =[easypath,mediumpath,hardpath,tutorialpath,quitpath]
   # main loop

   soundls[cond].play()
   while RUNNING:

     
      # Draw everything, adjust by offset
      screen.blit(victoryimage.image,list((0,0)))
      
      #Orb.update(WORLD_SIZE,gameClock)
      
      mousepos = pygame.mouse.get_pos()
      

      quill.position.x = mousepos[0]
      quill.position.y = mousepos[1]-quill.getHeight()
      quill.draw(screen)
      quit.draw(screen)
      # Flip the display to the monitor
      pygame.display.flip()
      
      # event handling, gets all event from the eventqueue


      for event in pygame.event.get():
            # only do something if the event is of type QUIT or ESCAPE is pressed

         rand = random.randint(0,1)


         if quit.getCollisionRect().collidepoint(mousepos[0],mousepos[1]):
            quit.image = pygame.image.load(quit1path)
            quit.image.set_colorkey(quit.image.get_at((0,0)))
         else:
               quit.image= pygame.image.load(quitpath)
               quit.image.set_colorkey(quit.image.get_at((0,0)))


                  
         if event.type == pygame.MOUSEBUTTONDOWN:


            if event.button == 1:
               #print(str((mousepos[0],mousepos[1])))


               if quit.getCollisionRect().collidepoint(mousepos[0],mousepos[1]):
                     RUNNING = False
         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            RUNNING = False
               

      # Update time and position
      gameClock.tick(60)
      ticks = gameClock.get_time() / 1000
      #Orb.position += Orb.velocity * ticks

      # # calculate offset
      # #offset = Vector2(max(0,
      #                      min(Orb.position.x + (Orb.image.get_width() // 2) - \
      #                          (SCREEN_SIZE[0] // 2),
      #                          WORLD_SIZE[0] - SCREEN_SIZE[0])),
      #                  max(0,
      #                      min(Orb.position.y + (Orb.image.get_height()// 2) - \
      #                          (SCREEN_SIZE[1] // 2),
      #                          WORLD_SIZE[1] - SCREEN_SIZE[1])))

      
      
      
      
  
      
   pygame.quit()



   
   
   
if __name__ == "__main__":
   Win()
