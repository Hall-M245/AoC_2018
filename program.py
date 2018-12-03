import re

def main():
    #day01_01()
    #day01_02()
    #day02_01()
    #day02_02()
    day03_01()

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
        for x in xrange(c.x, c.x+c.w):
            for y in xrange(c.y, c.y+c.h):
                fabric[x][y] += 1
    for x in xrange(fabricW):
        for y in xrange(fabricH):
            if(fabric[x][y] > 1):
                wastedSpace += 1
    print('Wasted fabric space: ' + str(wastedSpace))
    print('Inact fabric piece ID: ' + str(id))

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


if __name__ == '__main__':
    main()
