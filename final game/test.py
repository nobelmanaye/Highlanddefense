name = "Nobel"

namelst = []
poss = []

for letter in name: 
    namelst.append(letter)

for length in range(len(namelst)):
    for index in range(len(namelst)):
        if index +length < len(namelst):
            subset = [namelst[index]]

            for index2 in range(1,length+1,1):
                subset.append(namelst[index+index2])
        if subset not in poss:
            poss.append(subset)

print(poss)
