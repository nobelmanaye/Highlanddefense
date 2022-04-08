from Astar import astar


def rectangulate(Imageheight,Imagewidth,position):
    rectlst = []
    for x in range(round(position[0]),round(Imagewidth+position[0]),1):
       for y in range(round(position[1]),round(Imageheight+position[1]),1):
           rectlst.append((x,y))
    return rectlst





class graphmap (object):

    def __init__(self,screensize):    
        
        self.maze = []
        for y in range(screensize[1]):
            ls = []
            for x in range(screensize[0]):
                ls.append(0)
            self.maze.append(ls)
    def mark(self,Imageheight,Imagewidth,position):
        rectlst= rectangulate(Imageheight,Imagewidth,position)
        for item in rectlst:    
            self.maze[item[0]][item[1]] = 1
        
        
    def unmark(self,Imageheight,Imagewidth,position):
        rectlst= rectangulate(Imageheight,Imagewidth,position)
        for item in rectlst:    
            self.maze[item[0]][item[1]] = 0
    def __str__(self):
        strmaize = ""
        for row in self.maze:
            strrow = [str(pixel) for pixel in row]
            strmaize +=  (" ".join(strrow) + '\n')
            
        return  strmaize
            
    def astarpath(self,source,dest):
        return astar(self.maze,source,dest)
    
    


    

    #start = (0, 0)
    #end = (7, 6)

    #path = astar(maze, start, end)
    #print(path)


if __name__ == '__main__':
    a = graphmap([10,20])
    a.mark(3,4,[1,2])
    
    
    print(a.astarpath((0,0),(7,7)))

    
