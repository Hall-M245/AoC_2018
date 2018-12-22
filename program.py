import re
from datetime import datetime

def main():
    #day01_01()
    #day01_02()
    #day02_01()
    #day02_02()
    #day03_01()
    #day04_01()
    #day05_01()
    #day06_01()
    #day07_01()
    #day08_01()
    #day09()
    day10()

def day01_01():
    freq = 0
    with open('input/input_0101.txt', 'r') as inFile:
        line = inFile.readline()
        while line:
            freq += float(line)
            line = inFile.readline()
    print('Frequency: ' + str(freq))

def day01_02():
    freq = 0
    freqs = {}
    found = False
    while not(found):
        with open('input/input_0101.txt', 'r') as inFile:
            line = inFile.readline()
            while line:
                freq += float(line)
                if(freq in freqs):
                    line = None
                    found = True
                else:
                    freqs[freq] = 1
                    line = inFile.readline()
    print('Frequency: ' + str(freq))

def day02_01():
    numTwo = 0
    numThree = 0
    uniqueLetters = None
    with open('input/input_0201.txt', 'r') as inFile:
        line = inFile.readline().strip()
        while line:
            uniqueLetters = list(set(line))
            foundTwo = False
            foundThree = False
            for c in uniqueLetters:
                val = line.count(c)
                if(val == 2):
                    foundTwo = True
                if(val == 3):
                    foundThree = True
            if(foundTwo):
                numTwo += 1
            if(foundThree):
                numThree += 1
            line = inFile.readline().strip()
    print('Two: ' + str(numTwo) + ', Three: ' + str(numThree) + ', Checksum: ' + str(numTwo * numThree))

def day02_02():
    lines = []
    with open('input/input_0201.txt', 'r') as inFile:
        line = inFile.readline().strip()
        while line:
            lines.append(line)
            line = inFile.readline().strip()
    for thisLine in lines:
        for thatLine in lines:
            numErrors = 0
            firstError = -1
            for i in range(len(thisLine)):
                if(thisLine[i] != thatLine[i]):
                    numErrors += 1
                    firstError = i
            if(numErrors == 1):
                msg = ''
                for i in range(len(thisLine)):
                    if(i != firstError):
                        msg = msg + thisLine[i]
                print(msg)

def day03_01():
    fabricW = 1000
    fabricH = 1000
    fabric = [[0 for x in range(fabricW)] for y in range(fabricH)]
    claims = []
    wastedSpace = 0
    with open('input/input_0301.txt', 'r') as inFile:
        line = inFile.readline().strip()
        while line:
            claims.append(Claim(line))
            line = inFile.readline().strip()
    for c in claims:
        for x in range(c.x, c.x+c.w):
            for y in range(c.y, c.y+c.h):
                fabric[x][y] += 1
                if(fabric[x][y] > 1):
                    c.intact = False
    for x in range(fabricW):
        for y in range(fabricH):
            if(fabric[x][y] > 1):
                wastedSpace += 1
    print('Wasted fabric space: ' + str(wastedSpace))
    for c in claims:
        if(c.intact == True):
            for x in range(c.x, c.x+c.w):
                for y in range(c.y, c.y+c.h):
                    if(fabric[x][y] != 1):
                        c.intact = False
            if(c.intact == True):
                print('Inact fabric piece ID: ' + str(c.id))


class Claim:

    def __init__(self, valString):
        valString = valString.replace(' @ ',' ').replace(':','').replace('x',' ').replace(',',' ')
        vals = valString.split(' ')
        self.id = vals[0]
        self.x = int(vals[1])
        self.y = int(vals[2])
        self.w = int(vals[3])
        self.h = int(vals[4])
        self.intact = True

def day04_01():
    guards = {}
    activities = []
    with open('input/input_0401.txt', 'r') as inFile:
        line = inFile.readline().strip()
        while line:
            parts = line.replace('[','').split('] ')
            timeStamp = datetime.strptime(parts[0],'%Y-%m-%d %H:%M')
            act = parts[1]
            activities.append(Activity(act,timeStamp))
            line = inFile.readline().strip()
    activities.sort(key=lambda x: x.time)
    for item in activities:
        g = re.compile(r'\#\d{0,4}').findall(item.act)

        if(len(g) > 0):
            guardID = g[0].replace('#','')
            if(guardID in guards):
                currentGuard = guards[guardID]
            else:
                currentGuard = Guard(guardID)
                guards[guardID] = currentGuard
        elif(item.act == 'falls asleep'):
            item.guardO = currentGuard
            timeStart = item.time
        elif(item.act == 'wakes up'):
            item.guardO = currentGuard
            timeEnd = item.time
            sleepTime = int((timeEnd - timeStart).total_seconds()/60)
            currentGuard.totalSleepTime += sleepTime
            for x in range(timeStart.minute,timeEnd.minute):
                currentGuard.sleepMinutes[x] += 1
    bestGuard = None
    for g in guards:
        currentGuard = guards[g]
        if(bestGuard is None):
            bestGuard = currentGuard
        else:
            if(currentGuard.totalSleepTime > bestGuard.totalSleepTime):
                bestGuard = currentGuard
    print('Guard ' + str(bestGuard.id) + ' was asleep the longest with ' + str(bestGuard.totalSleepTime) + ' total asleep minutes.')
    bestTime = int(bestGuard.id) * int(bestGuard.sleepMinutes.index(max(bestGuard.sleepMinutes)))
    print('Best Guard Time: ' + str(bestTime))

    # Day 04 - Part 2
    bestGuard = None
    bestMinute = -1
    bestTime = 0
    for g in guards:
        currentGuard = guards[g]
        numTimes = max(currentGuard.sleepMinutes)
        minuteIndex = currentGuard.sleepMinutes.index(numTimes)
        if(bestGuard is None):
            bestGuard = currentGuard
            bestMinute = minuteIndex
            bestTime = numTimes
        else:
            if(numTimes > bestTime):
                bestGuard = currentGuard
                bestMinute = minuteIndex
                bestTime = numTimes
    print('Guard ' + str(bestGuard.id) + ' was asleep the most times on minute ' + str(bestMinute))
    print('Result: ' + str(int(bestGuard.id) * bestMinute))
            
class Guard:

    def __init__(self, id):
        self.id = id
        self.totalSleepTime = 0
        self.sleepMinutes = [0 for x in range(59)]

class Activity:

    def __init__(self,act,timeStamp):
        self.act = act
        self.time = timeStamp
        self.guardO = None

def day05_01():
    suitChain = ''
    with open('input/input_0501.txt', 'r') as inFile:
        line = inFile.readline().strip()
        while line:
            suitChain += line
            line = inFile.readline().strip()
    oldChain = suitChain
    newChain = ''
    complete = False
    regexCode = createChainRegEx()
    while (not complete):
        newChain = re.sub(regexCode,'',oldChain)
        if(newChain != oldChain):
            oldChain = newChain
        else:
            complete = True
    print('New Chain Length: ' + str(len(newChain)))

    smallestChain = -1
    polyList = 'abcdefghijklmnopqrstuvwxyz'
    for x in range(len(polyList)):
        oldChain = suitChain
        oldChain = oldChain.replace(polyList[x],'').replace(polyList[x].upper(),'')
        complete = False
        newChain = ''
        while (not complete):
            newChain = re.sub(regexCode,'',oldChain)
            if(newChain != oldChain):
                oldChain = newChain
            else:
                complete = True
        chainLength = len(newChain)
        if(smallestChain == -1):
            smallestChain = chainLength
        elif(chainLength < smallestChain):
            smallestChain = chainLength
    print('Smallest Chain Length: ' + str(smallestChain))

def createChainRegEx():
    reg = []
    a = 'abcdefghijklmnopqrstuvwxyz'
    for x in range(len(a)):
        reg.append(a[x] + a[x].upper())
        reg.append(a[x].upper() + a[x])
    msg = '|'.join([str(x) for x in reg])
    return(msg)

def day06_01():
    cities = dict()
    minX = 1000
    minY = 1000
    maxX = 0
    maxY = 0
    oFile = open('output.txt','w')
    cityID = 65
    with open('input/input_0601.txt', 'r') as inFile:
        line = inFile.readline().strip()
        while line:
            line = line.strip().replace(' ','')
            vals = line.split(',')
            if(len(vals) == 3):
                cities[vals[2]] = City(vals[0],vals[1],vals[2])
                #cities.append(City(vals[0],vals[1],vals[2]))
            else:
                cID = str(chr(cityID))
                cities[cID] = City(vals[0],vals[1],cID)
                #cities.append(City(vals[0],vals[1],str(chr(cityID))))
                cityID += 1
            line = inFile.readline().strip()
    # Determine the size of the city grid
    for city in cities:
        c = cities[city]
        if(c.x > maxX):
            maxX = int(c.x)
        if(c.y > maxY):
            maxY = int(c.y)
        if(c.x < minX):
            minX = int(c.x)
        if(c.y < minY):
            minY = int(c.y)
    for city in cities:
        c = cities[city]
        c.x -= minX
        c.y -= minY
    # Change maximums
    maxX -= minX -1 
    maxY -= minY -1 
    # Change grid minimums
    minX -= minX
    minY -= minY
    # Create the grid
    grid = []
    for y in range(maxY):
        gridRow = []
        grid.append(gridRow)
        for x in range(maxX):
            gridRow.append(Coordinate(x,y))
    # For each Coordinate in the grid, find the closest City
    for x in range(maxX):
        for y in range(maxY):
            for city in cities:
                c = cities[city]
                #oFile.write(grid[y][x].testCity(c) + '\n')
                grid[y][x].testCity(c)
    # Print Results
    safePointSize = 0
    for city in cities:
        c = cities[city]
        oFile.write(c.__str__() + '\t' + c.printResult() + '\n')
        #oFile.write('Points: \n')
        #oFile.write(c.printPoints() + '\n')
    oFile.write('\n/:   ') #0,1,2,3,4,5,6,7,8,9,0\n')
    oFile.write(','.join(str(x).zfill(3) for x in range(maxX)) + '\n')
    for y in range(maxY):
        rowStr = []
        for x in range(maxX):
            if(x == 0 or x == (maxX-1) or y == 0 or y == (maxY-1)):
                cID = grid[y][x].id
                if(cID != '.'):
                    cities[cID.upper()].valid = False
            if(grid[y][x].totalDistance < 10000):
                safePointSize += 1
            rowStr.append(grid[y][x].id.rjust(3))
        oFile.write(str(y).zfill(3) + ': ' + ','.join(rowStr) + '\n')
    # Final Result
    bestCity = None
    for city in cities:
        c = cities[city]
        if(c.validate(minX,minY,maxX-1,maxY-1)):
            if(bestCity is None):
                bestCity = c
            elif(c.numClosePoints > bestCity.numClosePoints):
                bestCity = c
    if(bestCity is None):
        oFile.write('Error: No best city.\n')
    else:
        oFile.write('Best City: ' + bestCity.__str__() + '\tNumber of Points: ' + bestCity.printResult() + '\n')
    oFile.write('Size of safest area: ' + str(safePointSize))
    oFile.close()

class Coordinate:

    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)
        self.closeCity = None # The closest city to this point
        self.closeDist = None # The distance to the closest city
        self.id = '.'
        self.totalDistance = 0

    def __str__(self):
        return ('Point: (' + str(self.x) + ',' + str(self.y) + ')')

    def __repr__(self):
        return ('Point: (' + str(self.x) + ',' + str(self.y) + ')')

    def testCity(self,c):
        deltaX = abs(self.x - c.x)
        deltaY = abs(self.y - c.y)
        distance = (deltaX + deltaY)
        self.totalDistance += distance
        # If there is no closest City set, then set this
        # City as the closest
        if(self.closeCity is None):
            self.closeCity = c
            self.closeDist = distance
            self.closeCity.modifyPoints(1,str(self.x)+','+str(self.y))
            if(distance == 0):
                self.id = c.id
            else:
                self.id = c.id.lower()
        # If this City is closer than the current City,
        # then set this City as the closest, additional
        # remove a point from the previous City
        elif(distance < self.closeDist):
            # The last City who was closest to this point, is no longer
            # the closest City, so decrement it's Point count.
            # *** Only do this if the ID is not already empty
            if(self.id != '.'):
                self.closeCity.modifyPoints(-1,str(self.x)+','+str(self.y))
            # This the new City as the closest city with the distance and
            # increment it's Point count
            self.closeCity = c
            self.closeDist = distance
            self.closeCity.modifyPoints(1,str(self.x)+','+str(self.y))
            # If this point is in fact the City's coordinates,
            # set this points ID to that of the City's
            if(distance == 0):
                self.id = self.closeCity.id
            else:
                self.id = self.closeCity.id.lower()
        elif(distance == self.closeDist):
            # If the current closest City and the new City are exactly
            # the same distance apart, then decrement the previous City's
            # Point count and reset this point's values and ID
            if(self.id != '.'):
                self.closeCity.modifyPoints(-1,str(self.x)+','+str(self.y))
                self.id = '.'
        return('City ' + c.id + ' is ' + str(distance) + ' unit(s) away from ' + self.__str__())

    def __eq__(self, that):
        if isinstance(that, Coordinate):
            if((self.x == that.x) and (self.y == that.y)):
                return True
            else:
                return False
        return False

    def __ne__(self, that):
        if isinstance(that, Coordinate):
            if((self.x == that.x) and (self.y == that.y)):
                return False
            else:
                return True
        return True

class City:

    def __init__(self,x,y,id='-'):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.numClosePoints = 0
        self.points = dict()
        self.valid = True

    def modifyPoints(self,val,point):
        self.numClosePoints += val
        if(val > 0):
            self.points[point] = True
        else:
            self.points[point] = False

    def validate(self,minX,minY,maxX,maxY):
        ret = False
        if(self.x <= minX):
            #print(self.__str__() + ' disqualified, most left city.')
            pass
        elif(self.x >= maxX):
            #print(self.__str__() + ' disqualified, most right city.')
            pass
        elif(self.y <= minY):
            #prit(self.__str__() + ' disqualified, most top city.')
            pass
        elif(self.y >= maxY):
            #print(self.__str__() + ' disqualified, most bottom city.')
            pass
        elif(self.valid == False):
            #print(self.__str__() + ' disqualified, infinite')
            pass
        else:
            # Does this City contain any points that are of the form
            # (x, 0) for x = 0 to maxX or (x, maxY) for x = 0 to maxX
            # (0, y) for y = 0 to maxY or (maxX, y) for y = 0 to maxY
            ret = True
        return ret

    def __str__(self):
        return ('City ' + str(self.id) + '\t(' + str(self.x) + ',' + str(self.y) + ')')

    def __repr__(self):
        return ('City ' + str(self.id) + '\t(' + str(self.x) + ',' + str(self.y) + ')')

    def printResult(self):
        return (str(self.numClosePoints))

    def printPoints(self):
        ret = []
        for p in self.points:
            if(self.points[p] == True):
                ret.append('\t(' + p + '): ' + str(self.points[p]))
        return ('\n'.join(ret))

def day07_01():
    verticies = dict()
    edges = []
    with open('input/input_0701.txt', 'r') as inFile:
        line = inFile.readline().strip()    
        while line:
            matches = re.findall(r'[s|S]tep [A-Z]?',line)
            if(matches.__len__() == 2):
                # Get the instructions IDs
                thisID = matches[0].split(' ')[1]
                thatID = matches[1].split(' ')[1]
                # Try and find a Vertext with thisID
                if(thisID not in verticies):
                    thisVertex = Vertex(thisID)
                    verticies[thisID] = thisVertex
                else:
                    thisVertex = verticies[thisID]
                # Try and find a Node with nextID
                if(thatID not in verticies):
                    thatVertex = Vertex(thatID)
                    verticies[thatID] = thatVertex
                else:
                    thatVertex = verticies[thatID]
                # Add the edge
                edges.append(Edge(thisVertex,thatVertex))
                # Associate Parents/Children
                thisVertex.addChild(thatVertex)
                thatVertex.addParent(thisVertex)
            line = inFile.readline().strip()
    # Test Printing
    oFile = open('output.txt','w')
    oFile.write('Verticies:\n')
    for v in verticies:
        oFile.write('\tVertex ' + str(verticies[v]) + '\n')
    oFile.write('Edges:\n')
    for e in edges:
        oFile.write('\tEdge ' + str(e) + '\n')
    # Construct Graph
    ex = Executor(verticies,5)
    oFile.write('Root Node: ' + str(ex.root) + '\n')
    oFile.write('Execute Order: ' + ''.join(ex.executeOrder()) + '\n')
    oFile.close()

class Executor:

    def __init__(self,verticies,numWork=1):
        self.verticies = verticies
        self.numWork = numWork
        self.root = self.findRoot()

    def findRoot(self):
        root = Vertex('.')
        for vID in self.verticies:
            v = self.verticies[vID]
            v.children.sort()
            if(v.parents.__len__() == 0):
                root.addChild(v)
        root.executed = True
        return root

    def executeOrder(self):
        oFile = open('outputTest.txt','w')
        allCodes = []
        exOrder = []
        q = []
        for child in self.root.children:
            q.append(child)
        currentTime = 0
        workers = []
        working = []
        # Create the Workers
        for x in range(self.numWork):
            workers.append(Elf(x))
        while q or working:
            # Check to see if any of the working elves have finished
            for w in working:
                # If the Elf is finished, update the instruction and place
                # the Elf back in the available workers pool
                if(w.endTime <= currentTime):
                    exOrder.append(w.currentStep.id)
                    w.currentStep.executed = True
                    for child in w.currentStep.children:
                        if(child.executed == False and child.id not in allCodes):
                            allCodes.append(child.id)
                            q.append(child)
                            child.checkReady()
                    w.reset()
                    working.remove(w)
                    workers.append(w)
            # Verify there is an available worker, else time advances
            flag = True
            while(workers and flag):
                q.sort() # Sort the Queue
                i = 0
                currNode = None
                # Find the next available Instruction, else time advances
                while currNode is None and i < len(q):
                    if q[i].checkReady() == True and q[i].executed != True:
                        currNode = q.pop(i)
                    else:
                        i += 1
                if(currNode is not None):
                    w = workers.pop() # The next available worker
                    w.work(currNode,currentTime) # Assign the Instruction to the worker
                    working.append(w) # The worker is now working
                else:
                    flag = False
            currentTime += 1
            oFile.write('Time: ' + str(currentTime-1) + ', Queue Length: ' + str(q.__len__()) + ', Working: ' + str(working.__len__()) + '\n')
        print('Time: ' + str(currentTime-2))
        return exOrder

class Vertex:

    def __init__(self,id):
        self.id = id
        self.children = []
        self.parents = []
        self.executed = False
        self.isReady = True

    def addChild(self,v):
        self.children.append(v)
    
    def addParent(self,v):
        self.parents.append(v)
        self.isReady = False

    def checkReady(self):
        val = True
        for p in self.parents:
            if(p.executed == False):
                val = False
        if(val == True):
            self.isReady = True
        else:
            self.isReady = False
        return self.isReady

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id
    
    def __eq__(self,that):
        if isinstance(that, Vertex):
            return self.id == that.id
        return False

    def __ne__(self,that):
        if isinstance(that, Vertex):
            return self.id != that.id
        return True
    
    def __lt__(self,that):
        if isinstance(that,Vertex):
            return self.id < that.id
        return False

    def __gt__(self,that):
        if isinstance(that,Vertex):
            return self.id > that.id
        return False
    
class Edge:

    def __init__(self,start=None,end=None):
        self.start = start
        self.end = end

    def __str__(self):
        return str(self.start) + ' --> ' + str(self.end)

    def __repr__(self):
        return str(self.start) + ' --> ' + str(self.end)

class Elf:

    def __init__(self,id=-1):
        self.id = id
        self.currentStep = None
        self.startTime = -1
        self.endTime = -1
        self.stepTime = 60

    def work(self,v,time):
        self.currentStep = v
        self.startTime = time
        self.endTime = self.stepTime + ord(v.id) + time - 64

    def reset(self):
        self.currentStep = None
        self.startTime = -1
        self.endTime = -1

    def status(self):
        return 'Worker ' + str(self.id) + ' working on ' + self.currentStep.id

def day08_01():
    q = None
    with open('input/input_0801.txt', 'r') as inFile:
        q = inFile.readline().strip().split(' ')
     
    tNodes = []
    processNode(q,tNodes)
    totalSum = 0
    oFile = open('output.txt','w+')
    for n in tNodes:
        oFile.write(str(n)+'\tMetadata: [' + ','.join([str(x) for x in n.metaData]) + ']\tNode Value: ' + str(n.nodeValue) + '\n')
        totalSum += sum(n.metaData)
    oFile.write('Metadata Sum: ' + str(totalSum) + '\n')
    oFile.write(tNodes[0].printTree(0))
    oFile.close()

def processNode(vals,tNodes,parent=None):
    
    # Create the new node
    c = int(vals.pop(0)) # Number of Children
    m = int(vals.pop(0)) # Number of Metadata
    n = tNode(c,m)
    tNodes.append(n)

    if(parent is not None):
        parent.children.append(n)

    # I am an internal node with children and metadata
    # Process all children
    if(c > 0):
        for i in range(c):
            vals = processNode(vals,tNodes,n)
            #n.children.append(tNodes[-1])
    # Now get my metadata
    for i in range(m):
        # The 0th metdata value = 1 points to 0th child
        v = int(vals.pop(0))
        n.metaData.append(v)
        if(n.id == '7'):
            print(v)
            print('Children:' + str(n.children.__len__()))
        if(v in range(0,len(n.children)+1)):
            n.nodeValue += n.children[v-1].nodeValue
        
        
    if(c == 0):
        n.nodeValue = sum(n.metaData)
    return vals

class tNode:

    idCount = 0
    def __init__(self,numChildren,numMeta):
        self.numChildren = numChildren
        self.numMeta = numMeta
        self.children = []
        self.metaData = []
        self.nodeValue = 0
        tNode.idCount += 1
        self.id = str(tNode.idCount)

    def __str__(self):
        return '\t'.join(['Node ' + self.id + ': ',str(self.numChildren),str(self.numMeta)])

    def __repr__(self):
        return '\t'.join(['Node ' + self.id + ': ',str(self.numChildren),str(self.numMeta)])
    
    def printTree(self,i):
        msg = ('\t'*i + 'Node ' + self.id + '[' + str(self.nodeValue) + ']\n')
        for c in self.children:
            msg += '\t'*(i+1) + c.printTree(i+1) + ''
        return msg

def day09():
    with open('input/input_09.txt', 'r') as inFile:
        line = inFile.readline().strip()
    matches = re.findall(r'[0-9]+',line)
    nPlayers = int(matches[0]) # Number of players
    nScore = int(matches[1]) # Value of the last score
    players = [Player() for x in range(nPlayers)] # List of players
    marbles = [] # List of marbles
    cPlayer = players[0] # Current player
    lMarble = Marble() # The last marble placed
    lScore = -1
    iMarble = lMarble # The inital marble
    cMarble = iMarble

    oFile = open('output.txt','w')
    # Play the game until all the marbles are gone
    oFile.write('Game\t' + 'Players ' + str(nPlayers) + ', Last Marble Worth ' + str(nScore) + '\n')
    while (cMarble.id != (nScore*100)):
        cMarble = Marble() # The current marble to be placed
        marbles.append(cMarble)
        if(cMarble.id % 23 == 0):
            lScore = cMarble.id
            cClock1 = lMarble.pMarble
            for x in range(0,6):
                cClock1 = cClock1.pMarble
            cClock2 = cClock1.pMarble
            clock1 = cClock1.nMarble
            cClock2.nMarble = clock1
            clock1.pMarble = cClock2
            lScore += cClock1.id
            cPlayer.score += (lScore)
            cMarble = clock1
        else:
            clock1 = lMarble.nMarble # First clockwise marble
            clock2 = lMarble.nMarble.nMarble # Second clockwise marble

            cMarble.pMarble = clock1
            cMarble.nMarble = clock2

            clock1.nMarble = cMarble 
            clock2.pMarble = cMarble

        lMarble = cMarble
        cPlayer = players[(cPlayer.id + 1) % nPlayers]
        
        if(cMarble.id == nScore):
            # Print score
            topScore = 0
            for p in players:
                oFile.write('Player ' + str(p.id) + '\tScore: ' + str(p.score) + '\n')
                if(int(p.score) > topScore):
                    topScore = int(p.score)
            oFile.write('Top Score: ' + str(topScore) + '\n')
            oFile.write('Current Marble Value: ' + str(cMarble.id) + '\n')
            oFile.write('Last Marble Value: ' + str(lScore) + '\n')
            oFile.close()
    
    # Print score
    topScore = 0
    for p in players:
        oFile.write('Player ' + str(p.id) + '\tScore: ' + str(p.score) + '\n')
        if(int(p.score) > topScore):
            topScore = int(p.score)
    oFile.write('Top Score: ' + str(topScore) + '\n')
    oFile.write('Current Marble Value: ' + str(cMarble.id) + '\n')
    oFile.write('Last Marble Value: ' + str(lScore) + '\n')
    oFile.close()

class Player:

    idCounter = 0

    def __init__(self):
        self.id = Player.idCounter
        self.score = 0
        Player.idCounter += 1

    def __str__(self):
        return ('Player ' + str(self.id) + ', Score: ' + str(self.score))
    
    def __repr__(self):
        return ('Player ' + str(self.id) + ', Score: ' + str(self.score))

class Marble:

    idCounter = 0

    def __init__(self):
        self.id = Marble.idCounter
        Marble.idCounter += 1
        self.pMarble = self # Pointer to prev marble
        self.nMarble = self # Pointer to next marble

    def __str__(self):
        return ('Marble ' + str(self.id))
    
    def __repr__(self):
        return ('Marble ' + str(self.id))

    def __eq__(self,that):
        if isinstance(that, Marble):
            return self.id == that.id
        return False

    def __ne__(self,that):
        if isinstance(that, Marble):
            return self.id != that.id
        return True

def day10():
    stars = []
    grid = dict()
    grid['minX'] = 1000000
    grid['minY'] = 1000000
    grid['maxX'] = -1000000
    grid['maxY'] = -1000000
    grid['maxV'] = 0
    with open('input/input_10.txt', 'r') as inFile:
        line = inFile.readline().strip()
        while line:
            s = Star(line)
            stars.append(s)
            # X-Values
            if(s.pos['x'] < grid['minX']):
                grid['minX'] = s.pos['x']
            if(s.pos['x'] > grid['maxX']):
                grid['maxX'] = s.pos['x']
            # Y-Values
            if(s.pos['y'] < grid['minY']):
                grid['minY'] = s.pos['y']
            if(s.pos['y'] > grid['maxY']):
                grid['maxY'] = s.pos['y']
            # Velocity
            if(abs(s.vel['x'] > grid['maxV'])):
                grid['maxV'] = abs(s.vel['x'])
            if(abs(s.vel['y'] > grid['maxV'])):
                grid['maxV'] = abs(s.vel['y'])
            line = inFile.readline().strip()
    print(grid)
    shiftX = grid['minX']
    shiftY = grid['minY']
    grid['maxX'] = grid['maxX'] - grid['minX']
    grid['minX'] = 0
    grid['maxY'] = grid['maxY'] - grid['minY']
    grid['minY'] = 0
    oFile = open('output.txt','w')
    oFile.write('Grid Size (X by Y) := (' + str(grid['maxX']) + ',' + str(grid['maxY']) + ')\n')
    # Star normalization
    for s in stars:
        s.pos['x'] -= shiftX
        s.pos['y'] -= shiftY
    # Time advance
    v = grid['maxV'] * 2
    for t in range(1):
        #sMap = [[' ' for y in range(grid['maxY']+v)] for x in range(grid['maxX']+v)]
        oFile.write('Time: ' + str(t) + '\n')
        for s in stars:
            pX = s.pos['x'] + (s.vel['x']*t)
            pY = s.pos['y'] + (s.vel['y']*t)
            #print(str(s.pos['x']) + ',' + str(s.pos['y']))
            #sMap[pY][pX] = '#'
        for y in range(grid['maxY']+v):
            oFile.write(str(y) + ':\t')
            for x in range(grid['maxX']+v):
                for s in stars:
                    pX = s.pos['x'] + (s.vel['x']*t)
                    pY = s.pos['y'] + (s.vel['y']*t)
                    if(pX == x and pY == y):
                        oFile.write('#')
                        break
                    else:
                        oFile.write('')
            oFile.write('\n')
        oFile.write('\n')
    oFile.close()

class Star():

    idCounter = 0
    def __init__(self,line):
        self.id = Star.idCounter
        Star.idCounter += 1
        matches = re.findall(r'-*[0-9]+',line)
        if(len(matches) == 4):
            self.pos = dict()
            self.pos['x'] = int(matches[0])
            self.pos['y'] = int(matches[1])
            self.vel = dict()
            self.vel['x'] = int(matches[2])
            self.vel['y'] = int(matches[3])

    def __str__(self):
        return ('Star ' + str(self.id))
    
    def __repr__(self):
        return ('Star ' + str(self.id))

if __name__ == '__main__':
    main()
