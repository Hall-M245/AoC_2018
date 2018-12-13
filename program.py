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
    day06_01()

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
    # Print Grid
    oFile.close()

class Coordinate:

    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)
        self.closeCity = None # The closest city to this point
        self.closeDist = None # The distance to the closest city
        self.id = '.'

    def __str__(self):
        return ('Point: (' + str(self.x) + ',' + str(self.y) + ')')

    def __repr__(self):
        return ('Point: (' + str(self.x) + ',' + str(self.y) + ')')

    def testCity(self,c):
        deltaX = abs(self.x - c.x)
        deltaY = abs(self.y - c.y)
        distance = (deltaX + deltaY)
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


if __name__ == '__main__':
    main()
