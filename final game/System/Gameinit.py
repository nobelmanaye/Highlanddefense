
def modecalc(mode):
      '''
      calculuates the game setting files ( when to finish, rate at which enemies come, number of enemies ) based on user input of game
       
      '''
      if mode =="tutorial":
         finished = False
         interval =60
         winminute = 3.3
         rate = 0.2
      if mode =="easy":
         scale =5
         finished = True
         interval = 50
         winminute = 5
         rate = 2

      if mode =="medium":
         finished = True
         scale = 3
         interval = 45
         winminute = 8
         rate = 6
      if mode == "hard":
         finished = True
         interval = 30
         winminute =10
         rate = 8
      else:
         finished = True
         interval = 30
         winminute =10
         winminute = 3.3

      return finished, interval,winminute,rate
