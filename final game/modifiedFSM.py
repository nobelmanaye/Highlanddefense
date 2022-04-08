class FSM(object):

    def __init__(self,states):
        
        self.statelst = list(states)
        self.state = statelst[0]
    def setState(self, state):
        '''
        Sets the state of the object
        '''
        self.state =state

    def getState(self,state):
        '''
        gets the state of the object
        '''
        self.state = state
    