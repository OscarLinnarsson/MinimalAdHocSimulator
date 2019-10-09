

import AHSNode
import AHSPacket
import AHSData
import AHSCacheFile
import AHSNodeLog
import toolbox as tb
import AHSSettings as settings

from random import randint
from random import shuffle
import copy


simulatedTrendStart = settings.simulatedTrendStart
simulatedTrendEnd = settings.simulatedTrendEnd
simulatedTrendIntervalX = settings.simulatedTrendIntervalX
simulatedTrendIntervalY = settings.simulatedTrendIntervalY

allNodes = []
cacheSize = settings.cacheSize
sideL = settings.sideL 
numTicks = settings.numTicks
avalibleFiles = settings.avalibleFiles


def startTrend(i):
    for x in range(simulatedTrendIntervalX[i][1]-simulatedTrendIntervalX[i][0]):
        for y in range(simulatedTrendIntervalY[i][1]-simulatedTrendIntervalY[i][0]):
            allNodes[x+simulatedTrendIntervalX[i][0]][y+simulatedTrendIntervalY[i][0]].startTrend(True)

def endTrend():
    for col in allNodes:
        for n in col:
            n.startTrend(False)

def getProbFileX():
    probMasLeft = 100
    tmpProbs = []
    for i in range(len(avalibleFiles)):
        tmp = randint(0, probMasLeft)
        probMasLeft = probMasLeft - tmp
        tmpProbs.append(tmp)
    shuffle(tmpProbs)
    sum = 0
    probs = []
    for prob in tmpProbs:
        sum += prob
        probs.append(sum)
    return probs

def newTick():
    for col in allNodes:
        for n in col:
            n.newTick()

def endTick():
    for col in allNodes:
        for n in col:
            n.endTick()

def tick(t):
    while t > 0:
        tb.ticksLeft = t
        for i in range(len(simulatedTrendEnd)):
            if (numTicks-t) == simulatedTrendEnd[i]:
                print("********************** END TREND")
                break
        for i in range(len(simulatedTrendStart)):
            if (numTicks-t) == simulatedTrendStart[i]:
                print("********************** START TREND")
                print("intervalX: {}-{}\tintervalY: {}-{}".format(simulatedTrendIntervalX[i][0], simulatedTrendIntervalX[i][1], simulatedTrendIntervalY[i][0], simulatedTrendIntervalY[i][1]))
                startTrend(i)
                break
        
        print("--------------------------------------------------------------------------------------")
        print("------------------------------------------------------------  Iterations left: {}".format(t))
        print("--------------------------------------------------------------------------------------")
        AHSNode.ticksSinceStart += 1
        newTick()
        forwardAllPackages()
        sendGetFileForRealCallbacks()
        endTick()
        t = t-1
        #allNodes[testX][testY].browsFreq = -10
    endSimulation()

def sendGetFileForRealCallbacks():
    for col in allNodes:
        for n in col:
            for fileReq in n.requestFileForReal:
                allNodes[fileReq.fromNodeX][fileReq.fromNodeY].sendFileForReal(fileReq)

def forwardAllPackages():
    for col in allNodes:
        for n in col:
            for p in n.toForward:
                if p.pType == 0:
                    GETforwardSinglePackage(n, p, n.x, n.y)
                elif p.pType == 1:
                    POSTforwardSinglePackage(n, p)
                elif p.pType == 2:
                    RESPONCEforwardSinglePackage(n, p, False)
                elif p.pType == 3:
                    RESPONCEforwardSinglePackage(n, p, True)

def POSTforwardSinglePackage(n, p):
    nodeX = n.x
    nodeY = n.y
    xDiff = p.toX - nodeX 
    yDiff = p.toY - nodeY
    if xDiff == 0:
        if p.toY > nodeY:
            n.tickLog.numSentPOST += forwardDown(p, nodeX, nodeY)
        else:
            n.tickLog.numSentPOST += forwardUp(p, nodeX, nodeY)
    elif yDiff == 0:
        if p.toX > nodeX:
            n.tickLog.numSentPOST +=  forwardRight(p, nodeX, nodeY)
        else:
            n.tickLog.numSentPOST +=  forwardLeft(p, nodeX, nodeY)
    else:
        if xDiff > 0:
            p.dirX = 1
        else:
            p.dirX = -1
        if yDiff > 0:
            p.dirY = -1
        else:
            p.dirY = 1
        n.tickLog.numSentPOST += forwardDiagonaly(p, nodeX, nodeY)


def RESPONCEforwardSinglePackage(n, p, withFile):
    nodeX = n.x
    nodeY = n.y
    xDiff = p.toX - nodeX 
    yDiff = p.toY - nodeY
    sentPackets = 0
    if abs(xDiff) > abs(yDiff):
        if p.toX > nodeX:
            sentPackets += forwardRight(p, nodeX, nodeY)
        else:
            sentPackets += forwardLeft(p, nodeX, nodeY)
    elif abs(xDiff) < abs(yDiff):
        if p.toY > nodeY:
            sentPackets += forwardDown(p, nodeX, nodeY)
        else:
            sentPackets += forwardUp(p, nodeX, nodeY)
    else:
        if xDiff > 0:
            p.dirX = 1
        else:
            p.dirX = -1
        if yDiff > 0:
            p.dirY = -1
        else:
            p.dirY = 1
        sentPackets += forwardDiagonaly(p, nodeX, nodeY)

    if withFile == True:
        n.tickLog.numSentFILE += sentPackets
    else:    
        n.tickLog.numSentRESPONCE += sentPackets


def GETforwardSinglePackage(n, p, nodeX, nodeY):
    sentPackets = 0
    if p.dirX == 0 and p.dirY == 0: # broadcast
        sentPackets += forwardUp(p, nodeX, nodeY)
        sentPackets += forwardDown(p, nodeX, nodeY)
        sentPackets += forwardLeft(p, nodeX, nodeY)
        sentPackets += forwardRight(p, nodeX, nodeY)
        sentPackets += forwardDiagonaly(p, nodeX, nodeY)
        n.tickLog.numSentGET += sentPackets
    else:
        refVal = p.dirX + p.dirY
        if refVal == 0 or refVal == -2 or refVal == 2:
            sentPackets += simpleForwards(p, nodeX, nodeY)
            sentPackets += forwardDiagonaly(p, nodeX, nodeY)
            n.tickLog.numSentGET += sentPackets
        else:
            sentPackets += simpleForwards(p, nodeX, nodeY)
            n.tickLog.numSentGET += sentPackets

def simpleForwards(p, nodeX, nodeY):
    retVal = 0
    if p.dirX == 1:
        retVal += forwardRight(p, nodeX, nodeY)
    elif p.dirX == -1:
        retVal += forwardLeft(p, nodeX, nodeY)
    if p.dirY == 1:
        retVal += forwardUp(p, nodeX, nodeY)
    elif p.dirY == -1:
        retVal += forwardDown(p, nodeX, nodeY)
    return retVal

def forwardUp(packet, nodeX, nodeY):
    p = copy.deepcopy(packet)
    if nodeY > 0:
        p.dirX = 0
        p.dirY = 1
        allNodes[nodeX][nodeY-1].incommingPacket(p)
        return 1
    return 0

def forwardDown(packet, nodeX, nodeY):
    p = copy.deepcopy(packet)
    if nodeY < sideL - 1:
        p.dirX = 0
        p.dirY = -1
        allNodes[nodeX][nodeY+1].incommingPacket(p)
        return 1
    return 0

def forwardLeft(packet, nodeX, nodeY):
    p = copy.deepcopy(packet)
    if nodeX > 0:
        p.dirX = -1
        p.dirY = 0
        allNodes[nodeX-1][nodeY].incommingPacket(p)
        return 1
    return 0

def forwardRight(packet, nodeX, nodeY):
    p = copy.deepcopy(packet)
    if nodeX < sideL - 1:
        p.dirX = 1
        p.dirY = 0
        allNodes[nodeX+1][nodeY].incommingPacket(p)
        return 1
    return 0

def forwardDiagonaly(packet, nodeX, nodeY):
    p = copy.deepcopy(packet)
    retVal = 0
    if p.dirX == 0 and p.dirY == 0:
        if nodeX + 1 < sideL and nodeY - 1 >= 0:
            p.dirX = 1
            p.dirY = 1
            allNodes[nodeX+1][nodeY-1].incommingPacket(p)
            retVal += 1
        if nodeX + 1 < sideL and nodeY + 1 < sideL:
            p.dirX = 1
            p.dirY = -1
            allNodes[nodeX+1][nodeY+1].incommingPacket(p)
            retVal += 1
        if nodeX - 1 >= 0 and nodeY - 1 >= 0:
            p.dirX = -1
            p.dirY = 1
            allNodes[nodeX-1][nodeY-1].incommingPacket(p)
            retVal += 1
        if nodeX - 1 >= 0 and nodeY + 1 < sideL:
            p.dirX = -1
            p.dirY = -1
            allNodes[nodeX-1][nodeY+1].incommingPacket(p)
            retVal += 1
        
    elif p.dirX == 1 and p.dirY == 1:
        if nodeX + 1 < sideL and nodeY - 1 >= 0:
            allNodes[nodeX+1][nodeY-1].incommingPacket(p)
            retVal += 1

    elif p.dirX == 1 and p.dirY == -1:
        if nodeX + 1 < sideL and nodeY + 1 < sideL:
            allNodes[nodeX+1][nodeY+1].incommingPacket(p)
            retVal += 1
            
    elif p.dirX == -1 and p.dirY == 1:
        if nodeX - 1 >= 0 and nodeY - 1 >= 0:
            allNodes[nodeX-1][nodeY-1].incommingPacket(p)
            retVal += 1
            
    elif p.dirX == -1 and p.dirY == -1:
        if nodeX - 1 >= 0 and nodeY + 1 < sideL:
            allNodes[nodeX-1][nodeY+1].incommingPacket(p)
            retVal += 1
            
    return retVal

def endSimulation():
    fileNameStr = "AdHocSimulatorLog - Policy {}.txt".format(settings.policy)
    print("")
    print("")
    print("************************************************")
    print("*****      SAVING SUMULATION TO FILE       *****")
    print("*****   {}   *****").format(fileNameStr)
    print("************************************************")
    print("")
    print("")
    newLogTxtFile = open(fileNameStr, "w") # w - write
    strToWrite = '{'
    strToWrite += settings.getJsonStr()
    
    strToWrite += '"allLogs" : ['
    for i in range(numTicks):
        strToWrite += '{ "allLogsOneTick" : ['
        for row in allNodes:
            for n in row:
                strToWrite += n.ticksLogArr[i].getJsonStr()
                strToWrite += ','
        strToWrite = strToWrite[:-1]
        strToWrite += ']},'        

    strToWrite = strToWrite[:-1]
    strToWrite += ']'
    strToWrite += '}'
    newLogTxtFile.write(strToWrite)
    newLogTxtFile.close()

    


for x in range(sideL):
    tmpNodeCol = []
    for y in range(sideL):
        n = AHSNode.node(False, x, y, randint(0, 30), getProbFileX(), cacheSize, [])
        tmpNodeCol.append(n)
    allNodes.append(tmpNodeCol)



gatewayServerX = 9
gatewayServerY = 9
cA = AHSCacheFile.cacheFile(AHSData.data(1, 99999, "A", 0, 13),  gatewayServerX, gatewayServerY)
cB = AHSCacheFile.cacheFile(AHSData.data(1, 99999, "B", 0, 13),  gatewayServerX, gatewayServerY)
cC = AHSCacheFile.cacheFile(AHSData.data(1, 99999, "C", 0, 13),  gatewayServerX, gatewayServerY)
cD = AHSCacheFile.cacheFile(AHSData.data(1, 99999, "D", 0, 13),  gatewayServerX, gatewayServerY)
ccE = AHSCacheFile.cacheFile(AHSData.data(1, 99999, "E", 0, 13), gatewayServerX, gatewayServerY)
ccF = AHSCacheFile.cacheFile(AHSData.data(1, 99999, "F", 0, 13), gatewayServerX, gatewayServerY)
ccG = AHSCacheFile.cacheFile(AHSData.data(1, 99999, "G", 0, 13), gatewayServerX, gatewayServerY)
ccH = AHSCacheFile.cacheFile(AHSData.data(1, 99999, "H", 0, 13), gatewayServerX, gatewayServerY)
ccI = AHSCacheFile.cacheFile(AHSData.data(1, 99999, "I", 0, 13), gatewayServerX, gatewayServerY)
ccJ = AHSCacheFile.cacheFile(AHSData.data(1, 99999, "J", 0, 13), gatewayServerX, gatewayServerY)

allNodes[gatewayServerX][gatewayServerY] = AHSNode.node(True, gatewayServerX, gatewayServerY, randint(0, 25), getProbFileX(), cacheSize, [cA, cB, cC, cD, ccE, ccF, ccG, ccH, ccI, ccJ])
tick(copy.deepcopy(numTicks))
