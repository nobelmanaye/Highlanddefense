 
class queue (object):

    def __init__(self):
        self.orderlst = []
        self.diction = {}
    def adding(self,gamepiece):
        
        self.orderlst.append(gamepiece)
    def draw(self,surface):
        blitorderlst = []
        IDlst = []
        self.diction = {}
        for gamepiece in self.orderlst: 
            intgamepiece = 2000- (gamepiece.position.y + gamepiece.getHeight())
            ID = str(intgamepiece) + str(gamepiece)
            IDlst.append(ID)
            self.diction[ID] = gamepiece
        IDlst.sort()
        
        print("ID " + str(IDlst))

        for pieceID in IDlst:
            self.diction[ID].draw(surface)

        
        


