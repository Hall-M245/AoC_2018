import re
from datetime import datetime

def main():
    #day01_01()
    #day01_02()
    #day02_01()
    #day02_02()
    #day03_01()
    day04_01()

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
            timeStart = item.time
        elif(item.act == 'wakes up'):
            timeEnd = item.time
            sleepTime = int((timeEnd - timeStart).total_seconds()/60)
            currentGuard.totalSleepTime += sleepTime
            if(sleepTime > currentGuard.longestSleep):
                currentGuard.longestSleep = sleepTime
                currentGuard.longestMin = timeStart.minute
    bestGuard = None
    for g in guards:
        currentGuard = guards[g]
        if(bestGuard is None):
            bestGuard = currentGuard
        else:
            if(currentGuard.totalSleepTime > bestGuard.totalSleepTime):
                bestGuard = currentGuard
    print('Guard ' + str(bestGuard.id) + ' was asleep for ' + str(bestGuard.totalSleepTime) + ' minutes, with the longest sleep starting at minute ' + str(bestGuard.longestMin) + '.')
    print('Result: ' + str(int(bestGuard.id) * int(bestGuard.longestMin)))

            
class Guard:

    def __init__(self, id):
        self.id = id
        self.totalSleepTime = 0
        self.longestSleep = 0
        self.longestMin = 0

class Activity:

    def __init__(self,act,timeStamp):
        self.act = act
        self.time = timeStamp

if __name__ == '__main__':
    main()
