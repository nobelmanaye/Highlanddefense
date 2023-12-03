import math



def Distance(start,end):
    
    squarex = start[0]-end[0]
    squarey = start[1]- end[1]
    
    return math.sqrt((squarex**2)+(squarey**2))
    
def rad(start,end):
    squarex = start[0]-end[0]
    squarey = start[1]- end[1]
    if squarex ==0:
        return 0
    return math.atan((squarey)/(squarex))
    
  
