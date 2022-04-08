

class Timer(object):
    def __init___(self,time,limit,action):
        self.starttime= time
        self.limit = limit
        self.action = action 
        self.done = False

        
        


    def do(self,time):
        if !self.done:
            diff = time -self.starttime
            if diff >= self.limit:
                self.action()  
                self.done = True     

    


        

        

        

    